__author__ = 'Jan Bogaerts'
__copyright__ = "Copyright 2016, AllThingsTalk"
__credits__ = []
__maintainer__ = "Jan Bogaerts"
__email__ = "jb@allthingstalk.com"
__status__ = "Prototype"  # "Development", or "Production"

from zwave import ZWave



import iotUserClient.attiotuserclient as IOT
from device import Device
from associations import Association
from groups import Group
import modules


class Gateway:
    def __init__(self, cloudData):
        self.json = cloudData
        self.modules = []                       #list of all the modules
        self.processors = []                    #list of all the processors
        self.protocols = []                     #supported protocol objects, example: ZWave (for referencing the functionality), loaded from the modules list
        self.devices = []
        self.groups = []
        self.associations = []
        self.loadData(self.json['id'])

    def addGroup(self, name):
        grp = Group(None)
        grp.name = name
        self.groups.append(grp)


    def loadData(self, id):
        """load devices, groups, ..."""
        fullDef = IOT.getGateway(id, True, True)
        self.loadPluginDefs(fullDef)
        self.devices = map(Device, [x for x in fullDef['devices'] if x['name'] != 'groups_groups'])
        self.loadAssociations(fullDef)
        self.loadScenes(fullDef)
        self.json = fullDef

    def loadPluginDefs(self, fullDef):
        self.modules = [x for x in fullDef['assets'] if x['name'] == 'modules']
        self.protocols = [x for x in fullDef['assets'] if x['name'] == 'protocols']
        for modName in self.modules:
            if modName in modules.modules:
                module = modules.modules[modName]
                if hasattr(module, "getProtocolManager"):
                    self.protocols.append(module.getProtocolManager())


    def loadAssociations(self, fullDef):
        """load all the assiosations defined on the device"""


