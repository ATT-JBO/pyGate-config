__author__ = 'Jan Bogaerts'
__copyright__ = "Copyright 2016, AllThingsTalk"
__credits__ = []
__maintainer__ = "Jan Bogaerts"
__email__ = "jb@allthingstalk.com"
__status__ = "Prototype"  # "Development", or "Production"



class ZWave:
    """protocol of hte gateway"""

    def getGeneral(self):
        """get the control shown on the general tab"""

    def getDeviceManagerControl(self):
        pass

    def getReset(self):
        pass


def getProtocolManager():
    """callback function for this plugin"""
    return ZWave()