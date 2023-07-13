from typing import List

from .modbus import Modbus


class ModbusRtu(Modbus):
    def __init__(self) -> None:
        super().__init__()
        raise NotImplementedError("Modbus RTU is not implemented")

    def modbus_rtu_connect(self) -> None:
        raise NotImplementedError("Modbus RTU is not implemented")

    def modbus_disconnect(self) -> None:
        raise NotImplementedError("Modbus RTU is not implemented")

    def read_register(self, address: int) -> int:
        raise NotImplementedError("Modbus RTU is not implemented")

    def read_multiple_registers(self, start_address: int, quantity: int) -> List[int]:
        raise NotImplementedError("Modbus RTU is not implemented")

    def write_register(self, address: int, value: int) -> None:
        raise NotImplementedError("Modbus RTU is not implemented")

    def write_multiple_registers(self, start_address: int, values: List[int]) -> None:
        raise NotImplementedError("Modbus RTU is not implemented")
