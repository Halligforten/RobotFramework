from libraries.Modbus.modbus_tcp import ModbusTcp

def show_main_menu(modbus_tcp : ModbusTcp) -> None:
    keep_running = True
    while keep_running:
        print("==================== Main ====================")
        print("1: Connect")
        print("2: Disconnect")
        print("3: Read parameter")
        print("4: Write parameter")
        print("5: Start heartbeat")
        print("6: Stop heartbeat")
        print("7: Clear error")
        print("8: Run")
        print("9: Stop")
        print("q: Exit program")

        choice = input("")

        if choice is "1":
            modbus_tcp.modbus_tcp_connect("192.168.1.10", 1)
        elif choice is "2":
            modbus_tcp.modbus_disconnect()
        elif choice is "3":
            parameter_index = int(input("Enter parameter index: "))
            parameter_value = modbus_tcp.modbus_read_register(parameter_index)
            print(f"{parameter_value}")
        elif choice is "4":
            parameter_index = int(input("Enter parameter index: "))
            parameter_value = int(input("Enter new value: "))
            parameter_value = modbus_tcp.modbus_write_register(
                parameter_index, parameter_value
            )
        elif choice is "5":
            modbus_tcp.modbus_start_heartbeat(250)
        elif choice is "6":
            modbus_tcp.modbus_stop_heartbeat()
        elif choice is "7":
            modbus_tcp.modbus_clear_error()
        elif choice is "8":
            run_direction = input("Enter direction (o=out, i=in): ")
            if run_direction == "o":
                modbus_tcp.modbus_run_out()
            elif run_direction == "i":
                modbus_tcp.modbus_run_in()
            else:
                print("Invalid direction!")
        elif choice is "9":
            modbus_tcp.modbus_stop_run()
        elif choice is "q":
            keep_running = False


def main() -> None:
    modbus_tcp = ModbusTcp()

    show_main_menu(modbus_tcp)
    modbus_tcp.modbus_disconnect()

if __name__ == "__main__":
    main()
