import socket
from time import sleep
from typing import List, Optional

import umodbus
import umodbus.client.tcp
from robot.api import logger

from .modbus import Modbus


class ModbusTcp(Modbus):
    def __init__(self):
        super().__init__()
        self.socket: Optional[socket.socket] = None

    def modbus_tcp_attempt_to_connect(
        self, ip_address: str, timeout: float, attempts: int
    ) -> None:
        connect_ok = False
        while not connect_ok:
            if attempts > 0:
                attempts -= 1
            else:
                raise RuntimeError("Could not connect")
            self.modbus_disconnect()
            self.modbus_tcp_connect(ip_address, timeout)
            if self.modbus_is_connected():
                try:
                    self.read_register(0x2001)
                    connect_ok = True
                except:
                    sleep(0.1)

    def modbus_tcp_connect(self, ip_address: str, timeout: float) -> None:
        if not self._is_connected:
            logger.info(f"Connecting: IP Address={ip_address}, Timeout={timeout} s")
            self.socket = socket.create_connection((ip_address, 502), timeout)
            self._is_connected = True
        else:
            raise RuntimeError("Modbus TCP is already connected")

    def modbus_disconnect(self) -> None:
        if self._is_connected:
            logger.info("Disconnect")
            if self.socket is not None:
                self.socket.shutdown(socket.SHUT_RDWR)
                self.socket.close()
            self._is_connected = False

    def read_register(self, address: int) -> int:
        if self._is_connected:
            message = umodbus.client.tcp.read_holding_registers(1, address, 1)
            response = umodbus.client.tcp.send_message(message, self.socket)
            value = response[0]
            logger.info(
                f"Read register: address={address}(0x{address:04x}), value={value}"
            )
            return value
        else:
            raise RuntimeError("Modbus TCP is not connected")

    def read_multiple_registers(self, start_address: int, quantity: int) -> List[int]:
        if self._is_connected:
            message = umodbus.client.tcp.read_holding_registers(
                1, start_address, quantity
            )
            response = umodbus.client.tcp.send_message(message, self.socket)
            values = response
            logger.info(
                f"Read multiple registers: start_address={start_address}(0x{start_address:04x}), quantity={quantity}, values={values}"
            )
            return values
        else:
            raise RuntimeError("Modbus TCP is not connected")

    def write_register(self, address: int, value: int) -> None:
        if self._is_connected:
            logger.info(
                f"Write register: address={address}(0x{address:04x}), value={value}"
            )
            message = umodbus.client.tcp.write_single_register(1, address, value)
            umodbus.client.tcp.send_message(message, self.socket)
        else:
            raise RuntimeError("Modbus TCP is not connected")

    def write_multiple_registers(self, start_address: int, values: List[int]) -> None:
        if self._is_connected:
            logger.info(
                f"Write multiple registers: start_address={start_address}(0x{start_address:04x}), values={values}"
            )
            message = umodbus.client.tcp.write_multiple_registers(
                1, start_address, values
            )
            umodbus.client.tcp.send_message(message, self.socket)
        else:
            raise RuntimeError("Modbus TCP is not connected")
