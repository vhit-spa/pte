import pylink as pk
from ..utils import MapParser
from logging import Logger

class MTMInterface():
    '''Micro To Machine interface class
    This class provide standarized way to interact to the micro via
    SEGGER J-Link interface. 
    For any issue please refer to the wrapped library:
    https://pylink.readthedocs.io/en/latest/index.html
    '''

    def __init__(self, serial_no:str, chip_name: str, logger: Logger, map_path: str) -> None:
        self._link: pk.JLink = pk.JLink()
        self._logger: Logger = logger
        self._serial_no: str = serial_no
        self._chip_name: str = chip_name

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