"""This module allows for execution and scheduling of calls in a separate thread."""

import time
import queue
import threading
import sched
import dataclasses
from typing import Any, Tuple
from dataclasses import dataclass, field


class ThreadWorker:
    """ThreadWorker allows for scheduling calls to an object.

    All calls happen in a separate thread which is started when a ThreadWorker
    object is created.

    The methods that wait will raise exceptions from the worker thread.
    """

    def __init__(self, obj):
        self._obj = obj
        self._lock = threading.Lock()
        self._scheduler = sched.scheduler()
        self._scheduler_thread = threading.Thread(
            target=self._scheduler_worker,
            args=(
                self._lock,
                self._scheduler,
            ),
            daemon=True,
        )
        self._scheduler_thread.start()

    def __enter__(self):
        self._lock.acquire()
        return self._obj

    def __exit__(self, exc_type, exc_value, tb):
        self._lock.release()

    @staticmethod
    def _scheduler_worker(lock, scheduler):
        max_delay = 0.01

        while True:
            with lock:
                next_event = scheduler.run(blocking=False)

            # Check for more events in `max_delay` time or wait unitl next one
            if next_event is not None:
                # Make sure that wait time is as short as possible and positive
                wait_time = max(min(max_delay, next_event), 0)
                time.sleep(wait_time)
            else:
                time.sleep(max_delay)

    def execute(self, fn, args=None):  # pylint: disable=invalid-name
        """Blocks the scheduler and executes the given function.

        Args:
            fn: Callable to be executed.  Takes the object as an argument.
            args: Additional arguments passed to the function.

        Returns:
            Forwards return from fn.
        """
        if args is None:
            args = tuple()

        with self._lock:
            return fn(self._obj, *args)

    def send(self, msg, delay=0, timeout=10):
        """Schedules the given message and waits until it has been executed.

        Shorthand for send_nowait(msg, delay).wait()
        See send_nowait().

        Returns:
            Forwards return from the message.
        """
        return self.send_nowait(msg, delay).wait(timeout)

    def send_nowait(self, msg, delay=0):
        """Schedules the given message on the worker thread.

        Args:
            msg: WorkerMessage object to schedule.
            delay: Optional execution delay (seconds)

        Returns:
            The passed message object.
        """
        self._scheduler.enter(delay, 1, msg.execute, (self._obj,))
        return msg

    def _reschedule(self, msg, delay, kill_ev):
        """Rescheduling routine for periodic()."""
        if not kill_ev.is_set():
            self._scheduler.enter(0, 2, msg.execute, (self._obj,))
            self._scheduler.enter(
                delay, 2, self._reschedule, (msg.next(), delay, kill_ev)
            )

    def periodic(self, msg, delay):
        """Schedules message for periodic execution.

        The next message object is retrieved with msg.next().

        Returns:
            Event which can be set to stop the execution.
        """
        kill_ev = threading.Event()

        self._reschedule(msg, delay, kill_ev)

        return kill_ev


@dataclass
class WorkerMessage:
    """Object representing a call.

    command(obj, *args).

    Args:
        command: Callable to be executed. Takes at least the object as an argument.
        args: Additional arguments.
    """

    command: Any
    args: Tuple = field(default_factory=tuple)
    _status_ok: threading.Event = field(init=False, default_factory=threading.Event)
    _status_exception: threading.Event = field(
        init=False, default_factory=threading.Event
    )
    _exception_q: queue.Queue = field(
        init=False, default_factory=lambda: queue.Queue(maxsize=1)
    )
    _q: queue.Queue = field(init=False, default_factory=lambda: queue.Queue(maxsize=1))
    _ev: threading.Event = field(init=False, default_factory=threading.Event)

    @property
    def status(self):
        """WorkerMessage status.

        Returns:
            None if the command has not been executed,
            True if the command has been executed,
            False if an exception was raised during execution.
        """
        if self._status_ok.is_set():
            return True
        if self._status_exception.is_set():
            return False
        return None

    def execute(self, obj):
        """Executes the object call.

        Note:
            This functions is meant to be called on the obj worker thread.
        """
        try:
            result = self.command(obj, *self.args)
            self._q.put(result)
            self._status_ok.set()
        except Exception as exception:  # pylint: disable=broad-except
            self._status_exception.set()
            self._exception_q.put(exception)
            self._q.put(None)
        finally:
            self._ev.set()

    def wait(self, timeout=10):
        """Wait until the call has been executed.

        Raises:
             Exception that happened on the worker thread.

        Returns:
            Forwards return from the call.
        """
        if not self._ev.wait(timeout):
            raise RuntimeError("WorkerMessage wait() timeout, could be stuck")

        try:
            raise self._exception_q.get(block=False)
        except queue.Empty:
            # no exception, nothing to do
            pass

        result = self._q.get(timeout)
        return result

    def next(self):
        """Returns next message."""
        return dataclasses.replace(self, command=self.command, args=self.args)
