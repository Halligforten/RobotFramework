import os
import sys
sys.path.insert(0, os.path.abspath('.'))
from libraries import Actuator

def main():
    actuator = Actuator()
    print(actuator.read("PARAMETER_0"))

if __name__ == "__main__":
    main()