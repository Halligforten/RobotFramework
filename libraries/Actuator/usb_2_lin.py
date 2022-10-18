from multiprocessing import Lock
from threading import Thread
from time import sleep
from typing import Dict

class Usb2Lin:
    STROKE_LENGTH = 500
    MAX_SPEED = 1
    EOS_OUT_INDEX = 0
    EOS_IN_INDEX = 1
    RUN_DIR_OUT_INDEX = 2
    RUN_DIR_IN_INDEX = 3

    def __init__(self) -> None:
        self.thread = Thread(target=self.threadFunction, daemon=True)
        self.lock = Lock()
        self.position = 0
        self.dummy_data : Dict[int, int] = {
            0 : 0,  # Position
            1 : 0,  # Status
            2 : 0,  # Run Cmd
            3 : 0,  # Target self.position
            4 : 0,  # Speed
        }     

    def start(self) -> None:
        self.thread.start()
    
    def get_lin_config(self, reference : int) -> int:
        with self.lock:
            value = self.dummy_data[reference]
        # print(f"Usb2Lin.get_lin_config - reference={reference}, value={value}")
        return value

    def set_lin_config(self, reference : int, value : int) -> None:
        # print(f"Usb2Lin.set_lin_config - reference={reference}, value={value}")
        with self.lock:
            self.dummy_data[reference] = value

    def threadFunction(self) -> None:
        while True:
            with self.lock:
                run_cmd = self.dummy_data[2]
                target_position = self.dummy_data[3]
                speed = self.dummy_data[4] / 100
            status = 0

            if run_cmd == 1:
                if self.position < self.STROKE_LENGTH:
                    self.position += speed
                    status |= (1 << self.RUN_DIR_OUT_INDEX)
            elif run_cmd == 2:
                if self.position > 0:
                    self.position -= speed
                    status |= (1 << self.RUN_DIR_IN_INDEX)
            elif run_cmd == 3:
                if self.position < target_position:
                    self.position += speed
                    if self.position >= target_position:
                        self.position = target_position
                    else:
                        status |= (1 << self.RUN_DIR_OUT_INDEX)
                elif self.position > target_position:
                    self.position -= speed
                    if self.position <= target_position:
                        self.position = target_position
                    else:
                        status |= (1 << self.RUN_DIR_IN_INDEX)

            if self.position >= self.STROKE_LENGTH:
                self.position = self.STROKE_LENGTH
                status |= (1 << self.EOS_OUT_INDEX)

            if self.position <= 0:
                self.position = 0
                status |= (1 << self.EOS_IN_INDEX)

            with self.lock:
                self.dummy_data[0] = int(self.position)
                self.dummy_data[1] = status
            sleep(0.01)
