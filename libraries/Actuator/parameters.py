from typing import Dict, List
from .usb_2_lin import Usb2Lin

class Parameters:      
    def __init__(self, usb_2_lin : Usb2Lin) -> None:
        self.usb_2_lin = usb_2_lin
        self.ini_name_to_reference_map : Dict[str, List[int]] = {
            "POSITION" : [0,16,0],
            "STATUS_EOS" : [1,2,0],
            "STATUS_RUN_DIR" : [1,2,2],
            "RUN_CMD" : [2,16,0],
            "TARGET_POSITION" : [3,16,0],
            "SPEED" : [4,16,0],
        }

    def read(self, ini_name : str) -> int:
        parameter_info = self.ini_name_to_reference_map[ini_name]
        value = self.usb_2_lin.get_lin_config(parameter_info[0])
        value = value >> parameter_info[2]
        value = value & ((1 << parameter_info[1]) - 1)
        # print(f"Parameters.read - ini_name={ini_name}, value={value}")
        return value

    def write(self, ini_name : str, value : int) -> None:
        # print(f"Parameters.write - ini_name={ini_name}, value={value}")

        parameter_info = self.ini_name_to_reference_map[ini_name]
        current = self.usb_2_lin.get_lin_config(parameter_info[0])
        current = current & ~(((1 << parameter_info[1]) - 1) << parameter_info[2])
        current = current | (value << parameter_info[2])
        self.usb_2_lin.set_lin_config(parameter_info[0], current)