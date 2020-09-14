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

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp

KEY_HOLDING_REG = "holding_registers"
KEY_BLOCK_NAME = "block_name"
KEY_REGISTERS = "registers"
KEY_ADDRESS = 'address'
KEY_VALUE = "value"
KEY_DISCRETE_IN = "digital_inputs"

def set_registers(path, client):
    print("set_registers: " + path)
    with open(path) as json_file:
        data = json.load(json_file)
        hold_regs = data[KEY_HOLDING_REG]
        hold_regs_block = hold_regs[KEY_BLOCK_NAME]
        client.add_block(hold_regs_block, cst.HOLDING_REGISTERS, 0, 200)
        for reg in hold_regs[KEY_REGISTERS]:
            addr = int(reg[KEY_ADDRESS])
            val = int(reg[KEY_VALUE], 16)
            client.set_values(hold_regs_block, addr, val)

        disc_regs = data[KEY_DISCRETE_IN]
        disc_regs_block = disc_regs[KEY_BLOCK_NAME]
        client.add_block(disc_regs_block, cst.DISCRETE_INPUTS, 0, 200)
        for reg in disc_regs[KEY_REGISTERS]:
            addr = int(reg[KEY_ADDRESS])
            val = int(reg[KEY_VALUE])
            client.set_values(disc_regs_block, addr, val)

def main():
    """main"""

    logger = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")

    try:
        #Create the server
        server = modbus_tcp.TcpServer()
        logger.info("running...")
        logger.info("enter 'quit' for closing the server")

        server.start()
        slave_1 = server.add_slave(1)
        set_registers('config.json', slave_1)
        
        #values = slave_1.get_values("0", 10, 2)
        #sys.stdout.write('done: values read: %s\r\n' % str(values))
        #testHex = '0xFF'
        #testHexInt = int(testHex, 16)
        #sys.stdout.write('done: values read: %s\r\n' % str(testHexInt))
        while True:
            cmd = sys.stdin.readline()
            args = cmd.split(' ')

            if cmd.find('quit') == 0:
                sys.stdout.write('bye-bye\r\n')
                break

            elif args[0] == 'add_slave':
                slave_id = int(args[1])
                server.add_slave(slave_id)
                sys.stdout.write('done: slave %d added\r\n' % slave_id)

            elif args[0] == 'add_block':
                slave_id = int(args[1])
                name = args[2]
                block_type = int(args[3])
                starting_address = int(args[4])
                length = int(args[5])
                slave = server.get_slave(slave_id)
                slave.add_block(name, block_type, starting_address, length)
                sys.stdout.write('done: block %s added\r\n' % name)

            elif args[0] == 'set_values':
                slave_id = int(args[1])
                name = args[2]
                address = int(args[3])
                values = []
                for val in args[4:]:
                    values.append(int(val))
                slave = server.get_slave(slave_id)
                slave.set_values(name, address, values)
                values = slave.get_values(name, address, len(values))
                sys.stdout.write('done: values written: %s\r\n' % str(values))

            elif args[0] == 'get_values':
                slave_id = int(args[1])
                name = args[2]
                address = int(args[3])
                length = int(args[4])
                slave = server.get_slave(slave_id)
                values = slave.get_values(name, address, length)
                sys.stdout.write('done: values read: %s\r\n' % str(values))

            else:
                sys.stdout.write("unknown command %s\r\n" % args[0])
    finally:
        server.stop()


if __name__ == "__main__":
    main()