import logging
import pylink as pk
from ..utils import MapParser
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
                 serial_no:int, 
                 chip_name: str, 
                 map_path: str,
                 logger_name: str = '__main__',
                ) -> None:
        self._link: pk.JLink = pk.JLink()
        self._serial_no: int = serial_no
        self._chip_name: str = chip_name
        self._logger: logging.Logger = logging.getLogger(logger_name)

        #Parse the map file and get the ICD
        self._map: MapParser = MapParser(src_path=map_path)
    
    def connect(self) -> bool:
        '''Wrapper of JLink connection methods'''
        try:
            # Open a connection to the J-Link
            self._link.open(self._serial_no)
            # Select the SWD target interface
            self._link.set_tif(pk.enums.JLinkInterfaces.SWD)
            # Connect to the target device
            self._link.connect(self._chip_name)

            self._logger.info("Connected successfully to the target micro")
            return True
        except Exception as e:
            self._logger.error("Connection failed: %s" % str(e))
            return False
        
    def sgn_write(self,signal_name: str, value: list) -> None:
        '''PyLink memory write wrapper

        [Inputs]
        - signal_name [str]: signal to be wrote
        - value [Any]:      new signal value

        [Output]
        - None
        '''
        sgn: dict = self._map.get_icd_data(signal_name)
        self._link.memory_write(addr=sgn['value'],data=value)

    def sgn_read(self,signal_name: str) -> Any:
        '''PyLink memory read wrapper

        [Inputs]
        - signal_name [str]: signal to be read

        [Output]
        - [Any]: signal values
        '''
        sgn: dict = self._map.get_icd_data(signal_name)
        res: list =  self._link.code_memory_read(addr=sgn['value'],num_bytes=sgn['size'])

        return res