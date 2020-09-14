#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""
 Modbus TestKit: Implementation of Modbus protocol in python

 (C)2009 - Luc Jean - luc.jean@gmail.com
 (C)2009 - Apidev - http://www.apidev.fr

 This is distributed under GNU LGPL license, see license.txt
"""

import sys
import json

import ModbusTcpServerAdapter as adapter
import modbus_tk
import modbus_tk.defines as cst
KEY_HOLDING_REG = "holding_registers"
KEY_BLOCK_NAME = "block_name"
KEY_REGISTERS = "registers"
KEY_ADDRESS = 'address'
KEY_VALUE = "value"
KEY_DISCRETE_IN = "digital_inputs"

def set_registers(path, server):
    print("set_registers: " + path)
    with open(path) as json_file:
        data = json.load(json_file)
        hold_regs = data[KEY_HOLDING_REG]
        hold_regs_block = hold_regs[KEY_BLOCK_NAME]
        server.add_block(1, hold_regs_block, cst.HOLDING_REGISTERS, 0, 200)
        for reg in hold_regs[KEY_REGISTERS]:
            addr = int(reg[KEY_ADDRESS])
            val = int(reg[KEY_VALUE], 16)
            server.set_register(1, hold_regs_block, addr, val)

        disc_regs = data[KEY_DISCRETE_IN]
        disc_regs_block = disc_regs[KEY_BLOCK_NAME]
        server.add_block(1, disc_regs_block, cst.DISCRETE_INPUTS, 0, 200)
        for reg in disc_regs[KEY_REGISTERS]:
            addr = int(reg[KEY_ADDRESS])
            val = int(reg[KEY_VALUE])
            server.set_register(1, disc_regs_block, addr, val)

def main():
    """main"""
    try:
        #Create the server
        server = adapter.ModbusTcpServerAdapter()

        server.start()
        server.add_client(1)
        set_registers('config.json', server)
        while True:
            cmd = sys.stdin.readline()
            args = cmd.split(' ')

            if cmd.find('quit') == 0:
                sys.stdout.write('bye-bye\r\n')
                break
            else:
                sys.stdout.write("unknown command %s\r\n" % args[0])
    finally:
        server.stop()


if __name__ == "__main__":
    main()