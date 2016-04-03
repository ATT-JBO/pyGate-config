__author__ = 'Jan Bogaerts'
__copyright__ = "Copyright 2016, AllThingsTalk"
__credits__ = []
__maintainer__ = "Jan Bogaerts"
__email__ = "jb@allthingstalk.com"
__status__ = "Prototype"  # "Development", or "Production"

from kivy.uix.screenmanager import Screen

#Defines all the functions that should be implemented by plugin modules

def getLabel():
    """return a label to represent the module. To include icons, use iconfonts.
    if this plugin does not have a screen, don't implement this function or return None.
    :rtype: basestring
    """

def getScreen():
    """returns the screen to show for editing this module's properties
    if this plugin does not have a view / screen, then return None or don't imlement this function.
    do the same for getLabel
    :rtype: Screen that has a function called 'updateData'. which is called whenever the currently active gateway is initially set / has changed
    """

def getProtocolManager():
    """returns a protocol manager object (see zwave), if this plugin supports a communication protocol
    that can include/exclude devices"""