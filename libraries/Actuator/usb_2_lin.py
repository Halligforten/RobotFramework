from threading import Thread
from time import sleep
from typing import Dict

class Usb2Lin:
    STROKE_LENGTH = 1000

    def __init__(self) -> None:
        self.thread = Thread(target=self.threadFunction, daemon=True)
        self.dummy_data : Dict[int, int] = {
            0 : 0,  # Position
            1 : 0,  # Status
            2 : 0,  # Run Cmd
        }     

    def start(self) -> None:
        self.thread.start()
    
    def get_lin_config(self, reference : int) -> int:
        value = self.dummy_data[reference]
        print(f"Usb2Lin.get_lin_config - reference={reference}, value={value}")
        return value

    def set_lin_config(self, reference : int, value : int) -> None:
        print(f"Usb2Lin.set_lin_config - reference={reference}, value={value}")
        self.dummy_data[reference] = value

    def threadFunction(self) -> None:
        while True:
            position = self.dummy_data[0]
            run_cmd = self.dummy_data[2]
            status = 0

            if run_cmd == 1:
                if position < self.STROKE_LENGTH:
                    position += 1
                    status |= (1 << 2)
            elif run_cmd == 2:
                if position > 0:
                    position -= 1
                    status |= (1 << 3)

            if position >= self.STROKE_LENGTH:
                position = self.STROKE_LENGTH
                status |= (1 << 0)

            if position <= 0:
                position = 0
                status |= (1 << 1)

            self.dummy_data[0] = position
            self.dummy_data[1] = status

            sleep(0.1)

