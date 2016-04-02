__author__ = 'Jan Bogaerts'
__copyright__ = "Copyright 2016, AllThingsTalk"
__credits__ = []
__maintainer__ = "Jan Bogaerts"
__email__ = "jb@allthingstalk.com"
__status__ = "Prototype"  # "Development", or "Production"


class AssetId():
    def __init__(self, **kwargs):
        if 'mod' in kwargs:
            self.module= kwargs['mod']
        else:
            self.module = ""
        if 'device' in kwargs:
            self.device = kwargs['device']
        else:
            self.device = ""
        if 'asset' in kwargs:
            self.asset = kwargs['asset']
        else:
            self.asset = ""