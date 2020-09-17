import sys
import json
from struct import *

from protocol_core.modbus.modbus_server_adapter import ModbusTkTcpServerAdapter
from protocol_core.modbus.modbus_engine import ModbusEngine
from protocol_core import defines as defs

from protocol_core.modbus.load_config import ConfigLoader

def load_model(model_path: str):
    with open(model_path) as json_file:
        data = json.load(json_file)
        registers = data["registers"]
        print("REGISTERS")
        print(registers)
        digital_inputs = data["digital_inputs"]
        print("DIGITAL")
        print(digital_inputs)
        id = data["id"]

def main():
    #load_model("config/config.json")
    loader = ConfigLoader()
    server_data = loader.load_model("config/config.json")
    adapter = ModbusTkTcpServerAdapter()
    engine = ModbusEngine(adapter)
    ret = engine.load_server(server_data)
    while True:
        cmd = sys.stdin.readline()
        args = cmd.split(' ')

        if cmd.find('quit') == 0:
            sys.stdout.write('bye-bye\r\n')
            break

if __name__ == "__main__":
    main()