__author__ = 'Jan Bogaerts'
__copyright__ = "Copyright 2016, AllThingsTalk"
__credits__ = []
__maintainer__ = "Jan Bogaerts"
__email__ = "jb@allthingstalk.com"
__status__ = "Prototype"  # "Development", or "Production"


from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen

from asset import AssetId
import data


def getLabel():
    """return a label to represent the module. To include icons, use iconfonts.
    if this plugin does not have a screen, don't implement this function or return None.
    :rtype: basestring
    """
    return 'associations'

def getScreen():
    """returns the screen to show for editing this module's properties
    if this plugin does not have a view / screen, then return None or don't imlement this function.
    do the same for getLabel
    :rtype: Screen that has a function called 'updateData'. which is called whenever the currently active gateway is initially set / has changed
    """
    return AssociationsScreen()



class Association(Widget):
    triggerId = StringProperty("")

    def __init__(self, **kwargs):
        if 'input' in kwargs:
            self.triggerId = kwargs['input']
        if 'outputs' in kwargs:
            self.outputs = [AssetId(mod=x['module'], device=x['device'], asset=x['asset']) for x in kwargs['outputs']]
        else:
            self.outputs = []


class AssociationsScreen(Screen):

    def updateData(self):
        fullDef = data.currentGateway.json
        asset = [x for x in fullDef['assets'] if x['name'] == 'associations']
        if len(asset) > 0:
            asset = asset[0]
            self.associations = [Association(input=key, outputs=value) for key, value in asset['state']['value'].iteritems()]