from typing import Dict

class Usb2Lin:
    def __init__(self) -> None:
        self.dummy_data : Dict[int, int] = {}
        for i in range(10):
            self.dummy_data[i] = 0

    def get_lin_config(self, reference : int) -> int:
        value = self.dummy_data[reference]
        print(f"Usb2Lin.get_lin_config - reference={reference}, value={value}")
        return value

    def set_lin_config(self, reference : int, value : int) -> None:
        print(f"Usb2Lin.set_lin_config - reference={reference}, value={value}")
        self.dummy_data[reference] = value