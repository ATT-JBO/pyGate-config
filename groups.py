__author__ = 'Jan Bogaerts'
__copyright__ = "Copyright 2016, AllThingsTalk"
__credits__ = []
__maintainer__ = "Jan Bogaerts"
__email__ = "jb@allthingstalk.com"
__status__ = "Prototype"  # "Development", or "Production"

from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, BooleanProperty
import json
import data


def getLabel():
    """return a label to represent the module. To include icons, use iconfonts.
    if this plugin does not have a screen, don't implement this function or return None.
    :rtype: basestring
    """
    return 'groups'

def getScreen():
    """returns the screen to show for editing this module's properties
    if this plugin does not have a view / screen, then return None or don't imlement this function.
    do the same for getLabel
    :rtype: Screen that has a function called 'updateData'. which is called whenever the currently active gateway is initially set / has changed
    """
    return GroupsScreen()

class GroupsScreen(Screen):
    def updateData(self):
        """update the data for the groups that should be displayed"""
        if data.currentGateway:
            fullDef = data.currentGateway.json
            groupsDev = [x for x in fullDef['devices'] if x['name'] == 'groups_groups']
            if len(groupsDev) > 0:
                groupsDev = groupsDev[0]
                asset = [x for x in groupsDev['assets'] if x['name'] == 'groupDefs']
                if len(asset) > 0:
                    asset = asset[0]
                    self.groups = map(Group, asset['state']['value'])


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

