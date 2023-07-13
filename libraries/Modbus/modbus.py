from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import IntEnum
from threading import Event
from typing import List

from threadworker import ThreadWorker, WorkerMessage


class PDU(IntEnum):
    heartbeat_counter = 0x2001
    run_cmd_position = 0x2002
    run_cmd_current = 0x2003
    run_cmd_speed = 0x2004
    run_cmd_soft_start = 0x2005
    run_cmd_soft_stop = 0x2006
    feedback_position = 0x2101
    feedback_current = 0x2102
    feedback_status_flags = 0x2103
    feedback_error_code = 0x2104
    feedback_speed = 0x2105
    feedback_input_state = 0x2106


class PositionCommand(IntEnum):
    clear_error = 0xFB00
    run_out = 0xFB01
    run_in = 0xFB02
    stop_run = 0xFB03
    recovery_run_out = 0xFB04
    recovery_run_in = 0xFB05


class ErrorCode(IntEnum):
    no_error = 0
    need_stop_command = 1
    hall_error = 2
    over_voltage = 3
    under_voltage = 4
    heartbeat_needed = 5
    eos_error = 6
    temperature_error = 7
    heart_beat_error = 8
    smps_error = 9
    current_measurement = 10
    parallel_arbitration_in_progress = 11
    internal_fault = 254
    external_fault = 255


@dataclass
class Modbus(ABC):
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        self._worker = ThreadWorker(self)
        self._stop_heartbeat_event = Event()
        self._heartbeat_counter = 0
        self._is_connected = False

    @abstractmethod
    def modbus_disconnect(self) -> None:
        pass

    def modbus_is_connected(self) -> bool:
        return self._is_connected

    def modbus_read_register(self, address: int) -> int:
        value = 0
        with self._worker as this:
            value = this.read_register(address)
        return value

    def modbus_read_multiple_registers(
        self, start_address: int, quantity: int
    ) -> List[int]:
        values = []
        if self._worker is not None:
            with self._worker as this:
                values = this.read_multiple_registers(start_address, quantity)
        return values

    def modbus_write_register(self, address: int, value: int) -> None:
        if self._worker is not None:
            with self._worker as this:
                this.write_register(address, value)

    def modbus_write_multiple_registers(
        self, start_address: int, values: List[int]
    ) -> None:
        if self._worker is not None:
            with self._worker as this:
                this.write_multiple_registers(start_address, values)

    def modbus_start_heartbeat(self, interval: int) -> None:
        if self._worker is not None:
            with self._worker as this:
                self.send_heartbeat(this)
            self._stop_heartbeat_event = self._worker.periodic(
                WorkerMessage(self.send_heartbeat), interval / 1000
            )
        else:
            raise RuntimeError("Modbus has not been initialized")

    def modbus_stop_heartbeat(self) -> None:
        self._stop_heartbeat_event.set()

    def modbus_run_out(self) -> None:
        self.modbus_write_register(PDU.run_cmd_position, PositionCommand.run_out)

    def modbus_run_in(self) -> None:
        self.modbus_write_register(PDU.run_cmd_position, PositionCommand.run_in)

    def modbus_run_to_position(self, target_position_mm: float) -> None:
        target_position_hall_counts = int(target_position_mm * 10)
        self.modbus_write_register(PDU.run_cmd_position, target_position_hall_counts)

    def modbus_stop_run(self) -> None:
        self.modbus_write_register(PDU.run_cmd_position, PositionCommand.stop_run)

    def modbus_clear_error(self) -> None:
        self.modbus_write_register(PDU.run_cmd_position, PositionCommand.clear_error)

    def modbus_get_eos_status(self) -> str:
        statusFlags = self.modbus_read_register(PDU.feedback_status_flags)
        eosIn = self.is_bit_set(statusFlags, 0)
        eosOut = self.is_bit_set(statusFlags, 1)

        if eosIn:
            formattedEosStatus = "in"
        elif eosOut:
            formattedEosStatus = "out"
        else:
            formattedEosStatus = "free"

        return formattedEosStatus

    def modbus_get_position(self) -> int:
        position = self.modbus_read_register(PDU.feedback_position)

        return position

    def modbus_get_current_consumption(self) -> int:
        current_consumption = self.modbus_read_register(PDU.feedback_current)

        return current_consumption

    def modbus_get_running_status(self) -> str:
        statusFlags = self.modbus_read_register(PDU.feedback_status_flags)
        runningOut = self.is_bit_set(statusFlags, 3)
        runningIn = self.is_bit_set(statusFlags, 4)

        if runningIn:
            formattedRunningStatus = "in"
        elif runningOut:
            formattedRunningStatus = "out"
        else:
            formattedRunningStatus = "stop"

        return formattedRunningStatus

    def modbus_get_error_code(self) -> str:
        error_code = self.modbus_read_register(PDU.feedback_error_code)
        return ErrorCode(error_code).name

    def modbus_get_position_lost(self) -> bool:
        position = self.modbus_read_register(PDU.feedback_position)

        return position == 65024

    def send_heartbeat(self, modbus: "Modbus"):
        modbus.write_register(PDU.heartbeat_counter, self._heartbeat_counter)
        self._heartbeat_counter += 1

    def is_bit_set(self, value, bitIndex: int) -> bool:
        is_set = ((value >> bitIndex) & 1) == 1
        return is_set

    @abstractmethod
    def read_register(self, address: int) -> int:
        pass

    @abstractmethod
    def read_multiple_registers(self, start_address: int, quantity: int) -> List[int]:
        pass

    @abstractmethod
    def write_register(self, address: int, value: int) -> None:
        pass

    @abstractmethod
    def write_multiple_registers(self, start_address: int, values: List[int]) -> None:
        pass
