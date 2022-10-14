from typing import Dict
from Usb2Lin import usb_2_lin

class Parameters:      
    def __init__(self, usb_2_lin : usb_2_lin.Usb2Lin) -> None:
        self.usb_2_lin = usb_2_lin
        self.ini_name_to_reference_map : Dict[str, int] = {}
        for i in range(10):
            self.ini_name_to_reference_map[f"PARAMETER_{i}"] = i

    def read(self, ini_name : str) -> int:
        value = self.usb_2_lin.get_lin_config(self.ini_name_to_reference_map[ini_name])
        print(f"Parameters.read - ini_name={ini_name}, value={value}")
        return value

    def write(self, ini_name : str, value : int) -> None:
        print(f"Parameters.write - ini_name={ini_name}, value={value}")
        self.usb_2_lin.set_lin_config(self.ini_name_to_reference_map[ini_name], value)