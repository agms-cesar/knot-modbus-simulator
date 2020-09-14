import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
from abc import ABC, abstractmethod

HOLDING = 0
DIGITAL = 1

class ModbusServerAdapter(ABC):
    def __init__(self):
        self.running = False
        super().__init__()

    @abstractmethod
    def start(self) -> bool:
        """Starts modbus' server adapter interface. """
        pass

    @abstractmethod
    def add_client(self, id) -> bool:
        pass

    @abstractmethod
    def add_block(self, client_id, name, block_type,
                  start_address, length) -> bool:
        pass
    
    @abstractmethod
    def set_register(self, client_id, block_name, address, value) -> bool:
        pass
    
    @abstractmethod
    def stop(self) -> bool:
        pass

class ModbusTcpServerAdapter(ModbusServerAdapter):

    block_type_map = {
        HOLDING : cst.HOLDING_REGISTERS,
        DIGITAL : cst.DISCRETE_INPUTS
    }

    def __init__(self):
        self.running = False
        self.tcp_server = None
        self.tcp_client = None
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

    def add_client(self, id):
        if self.running == True:
            try:
                self.tcp_server.add_slave(id)
                self.logger.info("Added tcp client with id = %d ", id)
                return True
            except:
                self.logger.error("Error while adding new client (id =%d)", id)
                return False

        else:
            self.logger.warning("Tcp server not running yet")
            return False

    def add_block(self, client_id, name, block_type, start_address, length):
        if self.running == True:
            try:
                client = self.tcp_server.get_slave(client_id)
                mapped_block = self.block_type_map[block_type]
                client.add_block(name, mapped_block, start_address,
                                 length)
                return True
            except:
                self.logger.error("Error occured while adding new block.")
                return False
        else:
            self.logger.warning("Tcp server not running yet.")
            return False
    
    def set_register(self, client_id, block_name, address, value):
        if self.running == True:
            try:
                client = self.tcp_server.get_slave(client_id)
                client.set_values(block_name, address, value)
                return True
            except:
                self.logger.error("Some error occurred while trying to add \
                    a value to block: %s", block_name)
                return False
        else:
            self.logger.warning("Tcp server not running yet.")
            return False
    
    def stop(self):
        if self.running == True:
            self.logger.info("Tcp server: Stopping...")
            self.tcp_server.stop()
            self.running = False
        else:
            self.logger.warning("Tcp server not running.")
        return True

