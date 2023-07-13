from random import Random
import socket
from time import sleep, time
from typing import Callable, List
from libraries.Modbus import Modbus
from libraries.Modbus.modbus_tcp import ModbusTcp
from pythonping import ping, executor
from libraries.Usb2Lin.usb_2_lin import Usb2Lin
from libraries.Ethernet import Ethernet

# from modbus import Modbus

def wait_until_no_error(modbus : Modbus, timeout : float) -> None:
    last_time = time()
    error_code = modbus.modbus_get_error_code()
    while error_code != "no_error":
        print(f"Waiting until no error - time remaining: {int(timeout * 1000)} ms")
        modbus.modbus_clear_error()
        error_code = modbus.modbus_get_error_code()
        if error_code != "no_error":
            now = time()
            delta_time = time() - last_time
            last_time = now
            timeout -= delta_time
            if timeout <= 0:
                raise RuntimeError("Could not clear error")
            sleep(0.1)

# def deinitialize_modbus(modbus : Modbus) -> None:
#     modbus.modbus_stop_run()
#     # modbus.modbus_tcp_disconnect()

def run_until_condition(modbus : Modbus, arguments : List[int], condition : Callable[[Modbus,List[int]], bool]):
    while not condition(modbus, arguments):
        print(f'position={modbus.modbus_get_position()}', end='\r', flush=True)
        sleep(0.05)

def run_duration(modbus : Modbus, duration : int) -> None:
    modbus.modbus_run_out()
    start_time = int(time())
    run_until_condition(modbus, [start_time, duration], run_duration_elapsed_condition)

def modbus_run_until_eos(modbus : Modbus, direction : int) -> None:
    if direction == 0:
        modbus.modbus_run_out()
    else:
        modbus.modbus_run_in()
    run_until_condition(modbus, [direction], reached_eos_condition)

def run_duration_elapsed_condition(modbus : Modbus, arguments : List[int]) -> bool:
    now = int(time())
    elapsed = now - arguments[0]
    return elapsed >= arguments[1]

def reached_eos_condition(modbus : Modbus, arguments : List[int]) -> bool:
    eos = modbus.modbus_get_eos_status()
    run_dir = modbus.modbus_get_running_status()
    return eos == {0:"out",1:"in"}.get(arguments[0]) and run_dir == "stop"

def connect_usb_lin(usb_2_lin : Usb2Lin) -> str:
    usb_2_lin.u2l_FindAllLinakDevices()
    device = usb_2_lin.LinakDevices[0]
    usb_2_lin.u2l_CloseDevice()
    sleep(0.2)
    usb_2_lin.u2l_OpenSpecificDevice(device)
    usb_2_lin.lin_UseSync(True)
    sleep(0.1)
    hardware_id = usb_2_lin.lin_ConnectAnyLinConfig(True)

    return hardware_id


def main():
    usb_2_lin = Usb2Lin()
    ethernet = Ethernet()

    hardware_id = connect_usb_lin(usb_2_lin)

    print(hardware_id)

    number_of_restarts_before = usb_2_lin.lin_GetLinConfig(16386)
    print(f"number_of_restarts_before = {number_of_restarts_before}")

    print("Activate CFG")
    usb_2_lin.lin_ActivateConfig()
    # sleep(1)

    print("Waiting for number of restarts to increase...")

    restart_done = False
    while not restart_done:
        sleep(0.01)
        number_of_restarts_after = usb_2_lin.lin_GetLinConfig(16386)
        print(f"number_of_restarts_after = {number_of_restarts_after}")
        restart_done = number_of_restarts_after = number_of_restarts_before + 1
        
    print("Restart done")

    sleep(2)

    print("Connecting...")

    start = time()
    could_connect = False
    while not could_connect:
        could_connect = ethernet.ethernet_can_connect_tcp("192.168.1.10", 502)

    end = time()
    delta = end - start
    print(delta)


if __name__ == "__main__":
    main()

    # modbus_tcp = ModbusTcp()
    # modbus_tcp.modbus_tcp_attempt_to_connect("192.168.1.10", 1, 5)

    # modbus_tcp.modbus_start_heartbeat(250)

    # wait_until_no_error(modbus_tcp, 10)
    # modbus_run_until_eos(modbus_tcp, 1)
    # modbus_run_until_eos(modbus_tcp, 0)
    # open_ports = ethernet.ethernet_scan_ports("192.168.1.10", 0, 65535)    
    # print(open_ports)