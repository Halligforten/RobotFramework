import socket
from typing import List


class Ethernet:
    def __init__(self) -> None:
        pass

    def ethernet_can_connect_tcp(self, ip_address: str, port: int) -> bool:
        could_connect = False
        s = socket.socket()
        socket.setdefaulttimeout(0.01)
        result = s.connect_ex((ip_address, port))
        if result == 0:
            could_connect = True
        s.close()
        return could_connect

    def ethernet_scan_ports(
        self, ip_address: str, first_port: int, last_port: int
    ) -> List[int]:
        open_ports = []
        for port in range(first_port, last_port):
            if self.ethernet_can_connect_tcp(ip_address, port):
                open_ports.append(port)
        return open_ports

    def ethernet_check_only_modbus_tcp_port_open(self, ip_address: str) -> bool:
        open_ports = self.ethernet_scan_ports(ip_address, 0, 65535)
        return (len(open_ports)) == 1 and (open_ports[0] == 502)
