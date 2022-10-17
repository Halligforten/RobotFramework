from libraries.Actuator import Actuator

def main():
    act = Actuator()

    act.write("RUN_CMD", 1)
   

if __name__ == "__main__":
    main()