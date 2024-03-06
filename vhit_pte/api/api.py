import pylink as pk
from ..utils import MapParser
from logging import Logger
from typing import Any

__all__ = ['MTMInterface']

class MTMInterface():
    '''Micro To Machine interface class
    This class provide standarized way to interact to the micro via
    SEGGER J-Link interface. 
    For any issue please refer to the wrapped library:
    https://pylink.readthedocs.io/en/latest/index.html
    '''

    def __init__(self, 
                 serial_no:str, 
                 chip_name: str, 
                 logger: Logger, 
                 map_path: str,
                 out_buff: int, 
                ) -> None:
        self._link: pk.JLink = pk.JLink()
        self._logger: Logger = logger
        self._serial_no: str = serial_no
        self._chip_name: str = chip_name
        self._out_buff_id: int = out_buff

        #Parse the map file and get the ICD
        self._map: MapParser = MapParser()
        self._map.parse(src_path=map_path)
    
    def connect(self) -> bool:
        '''Wrapper of JLink connection methods'''
        try:
            # Open a connection to the J-Link
            self._link.open(self.serial_no)
            #Select the SWD target interface
            self._link.set_tif(pk.enums.JLinkInterfaces.SWD)
            # Connect to the target device
            self._link.connect(self.chip_name)

            self._logger.info("Connected successfully to the target micro")
            return True
        except Exception as e:
            self._logger.error("Connection failed: %s" % str(e))
            return False
        
    def sgn_write(self,signal_name: str, value: Any) -> None:
        '''PyLink memory write wrapper

        [Inputs]
        - signal_name [str]: signal to be wrote
        - value [Any]:      new signal value

        [Output]
        - None
        '''
        self._link.memory_write(addr=self._map.icd[signal_name],data=value)

    def sgn_read(self,signal_name: str) -> Any:
        '''PyLink memory read wrapper

        [Inputs]
        - signal_name [str]: signal to be read

        [Output]
        - [Any]: signal values
        '''
        return self._link.memory_read(addr=self._map.icd[signal_name])