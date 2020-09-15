import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp

import protocol_core
from protocol_core.iserver_adapter import IServerAdapter

HOLDING = 0
DIGITAL = 1

class ModbusTkTcpServerAdapter(IServerAdapter):

    _block_type_map = {
        HOLDING : cst.HOLDING_REGISTERS,
        DIGITAL : cst.DISCRETE_INPUTS
    }

    def __init__(self):
        self.running = False
        self.tcp_server = None
        self.logger = modbus_tk.utils.create_logger(name="console",
            record_format="%(message)s")
    
    def __del__(self):
        if self.running == True:
            self.tcp_server.stop()
            self.running = False

    def start(self):
        """Starts modbus' server adapter interface. """
        try:
            self.tcp_server = modbus_tcp.TcpServer()
            self.tcp_server.start()
            self.running = True
            return self.running
        except:
            self.logger.error("Some error occurred while \
                creating a new tcp_server")
            self.tcp_server.stop()
            self.running = False
            return self.running

    def add_data_server(self, id):
        """ Adds a new modbus server """
        if self.running == True:
            try:
                self.tcp_server.add_slave(id)
                self.logger.info("Added modbus server with id = %d ", id)
                return True
            except:
                self.logger.error("Error while adding new server (id =%d)", id)
                return False

        else:
            self.logger.warning("Tcp server not running yet")
            return False

    def add_data_block(self, server_id, name, block_type,
                       start_address, length):
        """ Adds a new block of register to a modbuser server """
        if self.running == True:
            try:
                server = self.tcp_server.get_slave(server_id)
                mapped_block = self._block_type_map[block_type]
                if mapped_block == None:
                    return False
                server.add_block(name, mapped_block, start_address,
                                 length)
                return True
            except:
                self.logger.error("Error occured while adding new block.")
                return False
        else:
            self.logger.warning("Tcp server not running yet.")
            return False
    
    def set_data_value(self, server_id, block_name, address, value):
        """ Updates a modbus server register value """
        if self.running == True:
            try:
                server = self.tcp_server.get_slave(server_id)
                server.set_values(block_name, address, value)
                return True
            except:
                self.logger.error("Some error occurred while trying to add \
                    a value to block: %s", block_name)
                return False
        else:
            self.logger.warning("Tcp server not running yet.")
            return False
    
    def stop(self):
        """ Stops the tcp server and closes modbus servers
            connections """
        if self.running == True:
            self.logger.info("Tcp server: Stopping...")
            self.tcp_server.stop()
            self.running = False
        else:
            self.logger.warning("Tcp server not running.")
        return True

