from random import Random
from time import sleep
from typing import Callable, List
from libraries.Actuator import Actuator

def run_until_condition(actuator : Actuator, arguments : List[int], condition : Callable[[Actuator,List[int]], bool]):
    while not condition(actuator, arguments):
        print(f'position={actuator.read("POSITION")}, eos={actuator.read("STATUS_EOS")}, run_dir={actuator.read("STATUS_RUN_DIR")}', end='\r', flush=True)
        sleep(0.05)

def run_until_eos(actuator: Actuator, speed : int, direction : int) -> None:
    actuator.write("SPEED", speed)
    actuator.write("RUN_CMD", direction)
    
    run_until_condition(actuator, [direction], reached_eos_condition)

def run_until_target_position(actuator: Actuator, speed : int, target_position : int) -> None:
    print(f"Running to target position: {target_position} at speed: {speed}")
    actuator.write("SPEED", speed)
    actuator.write("TARGET_POSITION", target_position)
    actuator.write("RUN_CMD", 3)
    
    run_until_condition(actuator, [target_position], reached_target_position_condition)

def reached_eos_condition(actuator : Actuator, arguments : List[int]) -> bool:
    eos = actuator.read("STATUS_EOS")
    run_dir = actuator.read("STATUS_RUN_DIR")
    return eos == arguments[0] and run_dir == 0

def reached_target_position_condition(actuator : Actuator, arguments : List[int]) -> bool:
    position = actuator.read("POSITION")
    run_dir = actuator.read("STATUS_RUN_DIR")
    return position == arguments[0] and run_dir == 0


def main():
    actuator = Actuator()

    run_until_eos(actuator, 100, 1)      


    print('\n')

if __name__ == "__main__":
    main()