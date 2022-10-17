from .parameters import Parameters
from .usb_2_lin import Usb2Lin

class Actuator:
    def __init__(self) -> None:
        self.usb_2_lin = Usb2Lin()
        self.parameters = Parameters(self.usb_2_lin)
        self.usb_2_lin.start()
    
    def read(self, ini_name : str) -> int:
        value = self.parameters.read(ini_name)
        print(f"Actuator.read - ini_name={ini_name}, value={value}")
        return value

    def write(self, ini_name : str, value : int) -> None:
        print(f"Actuator.write - ini_name={ini_name}, value={value}")
        self.parameters.write(ini_name, value)