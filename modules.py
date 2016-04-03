__author__ = 'Jan Bogaerts'
__copyright__ = "Copyright 2016, AllThingsTalk"
__credits__ = []
__maintainer__ = "Jan Bogaerts"
__email__ = "jb@allthingstalk.com"
__status__ = "Prototype"  # "Development", or "Production"

import logging

modules = {}                                    # the list of dynamically loaded modules.

activeActionItems = []                          # the action bar items that are loaded for the currentlya active view (module)


def load(moduleNames):
    """Loads all the gateway modules"""
    global modules
    logging.info("loading modules")
    modules = dict(zip(moduleNames, map(__import__, moduleNames)))       # load the modules and put them in a dictionary, key = the name of the module.