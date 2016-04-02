__author__ = 'Jan Bogaerts'
__copyright__ = "Copyright 2016, AllThingsTalk"
__credits__ = []
__maintainer__ = "Jan Bogaerts"
__email__ = "jb@allthingstalk.com"
__status__ = "Prototype"  # "Development", or "Production"

from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, BooleanProperty
import json

class Group(Widget):
    name = StringProperty("")
    description = StringProperty("")
    profile = StringProperty("")
    sleep = NumericProperty(0.1)        # nr of seconds between each actuator that gets triggered when the group is triggered
    def __init__(self, data, **kwargs):
        self.json = data
        if data:
            self.name = data['name']
            self.description = data['description']
            self.profile = json.dumps(data['profile'])
            self.sleep = data['sleep']
            self.actuators = data['actuators']
        else:
            self.actuators = []

