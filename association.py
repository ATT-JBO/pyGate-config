__author__ = 'Jan Bogaerts'
__copyright__ = "Copyright 2016, AllThingsTalk"
__credits__ = []
__maintainer__ = "Jan Bogaerts"
__email__ = "jb@allthingstalk.com"
__status__ = "Prototype"  # "Development", or "Production"


from kivy.uix.widget import Widget
from kivy.properties import StringProperty

from asset import AssetId

class Association(Widget):
    triggerId = StringProperty("")

    def __init__(self, **kwargs):
        if 'input' in kwargs:
            self.triggerId = kwargs['input']
        if 'outputs' in kwargs:
            self.outputs = [AssetId(mod=x['module'], device=x['device'], asset=x['asset']) for x in kwargs['outputs']]
        else:
            self.outputs = []

