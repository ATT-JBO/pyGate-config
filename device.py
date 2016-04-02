__author__ = 'Jan Bogaerts'
__copyright__ = "Copyright 2016, AllThingsTalk"
__credits__ = []
__maintainer__ = "Jan Bogaerts"
__email__ = "jb@allthingstalk.com"
__status__ = "Prototype"  # "Development", or "Production"

from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, BooleanProperty

class Device(Widget):
    """represents a single device"""
    location = StringProperty("")
    name = StringProperty("")
    dead = BooleanProperty(False)            # battery powered devices that can't be found anymore
    batteryLevel = NumericProperty(100)
    isBattery = BooleanProperty(False)
    deviceType = StringProperty("unknown")      # zwave, xbee,... -> module of the device

    def __init__(self, json, **kwargs):
        self.json = json
        for asset in json['assets']:
            # assetName = str(asset['name'])
            if asset['style'] == 'battery':
                self.isBattery = True
                self.batteryLevel = asset['state']['value']
            elif asset['name'] == 'location':
                self.location = asset['state']['value']
        self.name = json['label']
        self.deviceType = str(json['name']).split['_'][0]



    def delete(self):
        """delete this device or start the exclude process and ask the user to press the button on the device
        if the device is marked as 'dead', send the remove instruction."""