__author__ = 'Jan Bogaerts'
__copyright__ = "Copyright 2016, AllThingsTalk"
__credits__ = []
__maintainer__ = "Jan Bogaerts"
__email__ = "jb@allthingstalk.com"
__status__ = "Prototype"  # "Development", or "Production"

from zwave import ZWave
from iotUserClient.popups.credentials import Credentials
from iotUserClient.popups.claimGateway import ClaimGatewayDialog
import iotUserClient.attiotuserclient as IOT
from device import Device
from association import Association
from group import Group

class Data:
    def __init__(self):
        self.gateways = []
        self.grounds = []
        self.currentGround = None
        self.credentials = Credentials()

    def claimGateway(self, claimcode, groundId):
        '''sends the claimcode to the cloud and adds the related gateway object to the list and returns it.
        '''
        dlg = ClaimGatewayDialog(self.onGatewayClaimed)
        dlg.claim(groundId, claimcode)

    def onGatewayClaimed(self, gateway):
        self.gateways.append(Gateway(gateway))

    def scanGrounds(self):
        """list all the grounds in the account"""
        self.grounds = IOT.getGrounds(False)
        for ground in self.grounds:
            self.scanGateways(ground['id'])

    def scanGateways(self, groundId):
        """scan the account for all gateways."""
        gateways = IOT.getGateways(groundId)
        for gateway in gateways:
            try:
                id = IOT.getAssetByName(gateway['id'], 'applicationId')
            except:
                id = None
            if id and 'State' in id and id['State']['Value'] and str(id['State']['Value']) == "ATT-pyGate":
                self.gateways.append(Gateway(gateway))


class Gateway:
    def __init__(self, cloudData):
        self.json = cloudData
        self.protocols = [ZWave()]
        self.devices = []
        self.groups = []
        self.associations = []

    def addGroup(self, name):
        grp = Group(None)
        grp.name = name
        self.groups.append(grp)


    def loadData(self):
        """load devices, groups, ..."""
        fullDef = IOT.getGateway(self.json['id'], True, True)
        self.devices = map(Device, [x for x in fullDef['devices'] if x['name'] != 'groups_groups'])
        self.loadGroups(fullDef)
        self.loadAssociations(fullDef)
        self.loadScenes(fullDef)

    def loadGroups(self, fullDef):
        """load all the groups defined in the device"""
        groupsDev = [x for x in fullDef['devices'] if x['name'] == 'groups_groups']
        if len(groupsDev) > 0:
            groupsDev = groupsDev[0]
            asset = [x for x in groupsDev['assets'] if x['groupDefs']]
            if len(asset) > 0:
                asset = asset[0]
                self.groups = map(Group, asset['state']['value'])

    def loadAssociations(self, fullDef):
        """load all the assiosations defined on the device"""
        asset = [x for x in fullDef['assets'] if x['name'] == 'associations']
        if len(asset) > 0:
            asset = asset[0]
            self.associations = [Association(input=key, outputs=value) for key, value in asset['state']['value'].iteritems()]




data = Data()