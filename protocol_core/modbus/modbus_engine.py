#o que o modbusEngine vai fazer?

# Vai criar o server adapter
# Vai guardar os registers criados
# Vai setar os regs
from .modbus_server_adapter import ModbusTkTcpServerAdapter
import ..defs as defs

class ModbusEngine:
    _adapter = None
    _things_map = []
    def __init__(self, adapter: ModbusTkTcpServerAdapter):
        self._adapter = adapter
        ret = adapter.start()
        if ret != True:
            raise InterruptedError("Unable to start tcp server")
        self._has_things = False
    
    def load_things(self, things) -> bool:
        """ Carrega uma lista de things e cria os blocos no
            servidor de modbus """
        self._things_map.clear()
        self._has_things = False
        id = 0
        for thing in things:
            data = {}
            data = thing
            id = thing[defs.THING_ID]
            name = thing[defs.THING_NAME]
            address = thing[defs.THING_ADDRESS]
            offset = thing[defs.THING_OFFSET]
            if id == None or name == None or address == None \
            or offset == None:
                self._things_map.clear()
                return False
            
    def set_things_values(self, things_values) -> bool:
        """ Seta os valores das things """

    def _update(self) -> bool:
        """ Atualiza os valores dos registradores do servidor modbus 
            com os valores atuais das things periodicamente """
    
    def set_update_timer(self, timeout):
        """ Seta os valor de timeout para atualizar os registers
            do modbus """
            
            
            



