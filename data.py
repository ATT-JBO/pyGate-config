__author__ = 'Jan Bogaerts'
__copyright__ = "Copyright 2016, AllThingsTalk"
__credits__ = []
__maintainer__ = "Jan Bogaerts"
__email__ = "jb@allthingstalk.com"
__status__ = "Prototype"  # "Development", or "Production"

import logging
from ConfigParser import *

from iotUserClient.popups.credentials import Credentials
from iotUserClient.popups.claimGateway import ClaimGatewayDialog
import iotUserClient.attiotuserclient as IOT
from gateway import Gateway

gateways = []
currentGateway = None
grounds = []
moduleNames = []
credentials = Credentials()
configs = ConfigParser()

appConfigFileName = 'app.config'


def loadSettings():
    global moduleNames
    if configs.read(appConfigFileName):
        if configs.has_option('general', 'modules'):
            modulesStr = configs.get('general', 'modules')
            logging.info("modules: " + str(modulesStr))
            moduleNames = [x.strip() for x in modulesStr.split(';')]
        if configs.has_option('general', 'username'):
            credentials.userName = configs.get('general', 'username')
        if configs.has_option('general', 'password'):
            credentials.password = configs.get('general', 'password')
        if configs.has_option('general', 'server'):
            credentials.server = configs.get('general', 'server')
        if configs.has_option('general', 'broker'):
            credentials.broker = configs.get('general', 'broker')
        if configs.has_option('general', 'secure'):
            credentials.secure = configs.get('general', 'secure')

def getSetting(section, name, default = None):
    if configs.has_option(section, name):
        return configs.get('general', 'username')
    else:
        return default

def saveSettings():
    if not configs.has_section('general'):
        configs.add_section('general')
    configs.set('general', 'username', credentials.userName)
    configs.set('general', 'password', credentials.password)
    configs.set('general', 'server', credentials.server)
    configs.set('general', 'broker', credentials.broker)
    configs.set('general', 'modules', ';'.join(moduleNames))
    if currentGateway:
        configs.set('general', 'current gateway', currentGateway.json['id'])
    else:
        configs.set('general', 'current gateway', None)
    with open(appConfigFileName, 'w') as f:
        configs.write(f)

def claimGateway( claimcode, groundId):
    '''sends the claimcode to the cloud and adds the related gateway object to the list and returns it.
    '''
    dlg = ClaimGatewayDialog(onGatewayClaimed)
    dlg.claim(groundId, claimcode)


def onGatewayClaimed(gateway):
    gateways.append(Gateway(gateway))


def scanGrounds():
    """list all the grounds in the account"""
    global currentGateway
    currentGateway = None               #reset the current gateway, if we find the correct id in the new account, then set that as the active one.
    grounds = IOT.getGrounds(False)
    for ground in grounds:
        scanGateways(ground['id'])


def scanGateways(groundId):
    """scan the account for all gateways."""
    global currentGateway
    currentId = getSetting('general', 'current gateway')
    gateways = IOT.getGateways(groundId)
    for gateway in gateways:
        try:
            id = IOT.getAssetByName(gateway['id'], 'applicationId')
        except:
            id = None
        if id and 'State' in id and id['State']['Value'] and str(id['State']['Value']) == "ATT-pyGate":
            toAdd = Gateway(gateway)
            gateways.append(toAdd)
            if currentId and currentId == toAdd.json['id']:
                currentGateway = toAdd