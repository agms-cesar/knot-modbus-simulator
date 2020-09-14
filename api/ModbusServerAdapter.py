from abc import ABC

class ModbusServerAdapter(ABC):
    def __init__(self):
        self.running = False

    def start(self) -> bool:
        """Starts modbus' server adapter interface. """
        pass

    def add_client(self, id) -> bool:
        pass

    def add_block(self, client_id, name, block_type,
                  start_address, length) -> bool:
        pass
    
    def set_register(self, client_id, block_name, address, value) -> bool:
        pass
    
    def stop(self) -> bool:
        pass