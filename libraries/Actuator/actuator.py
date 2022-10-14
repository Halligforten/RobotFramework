from Usb2Lin import usb_2_lin
from Parameters import parameters

class Actuator:
    def __init__(self) -> None:
        self.usb_2_lin = usb_2_lin.Usb2Lin()
        self.parameters = parameters.Parameters(self.usb_2_lin)
    
    def read(self, ini_name : str) -> int:
        value = self.parameters.read(ini_name)
        print(f"Actuator.read - ini_name={ini_name}, value={value}")
        return value

    def write(self, ini_name : str, value : int) -> None:
        print(f"Actuator.write - ini_name={ini_name}, value={value}")
        self.parameters.write(ini_name, value)