__author__ = 'Jan Bogaerts'
__copyright__ = "Copyright 2016, AllThingsTalk"
__credits__ = []
__maintainer__ = "Jan Bogaerts"
__email__ = "jb@allthingstalk.com"
__status__ = "Prototype"  # "Development", or "Production"

from kivy.uix.treeview import TreeView, TreeViewLabel

import iotUserClient.attiotuserclient as IOT
from errors import *

class AssetsTreeView(TreeView):
    """
        create_node_func: assign a callback function so that you can filter items and create custom widgets.
         signature: create_node_func(obj, type, parent) where obj is a json structure and type is 'ground', 'device' or 'asset' and parent is the parent node (if any)
    """
    def __init__(self, **kwargs):
        self.load_func = self.populateTreeNode
        self.create_node_func = None                #
        super(AssetsTreeView, self).__init__(**kwargs)

    def populateTreeNode(self, treeview, node):
        try:
            if not node:
                grounds = IOT.getGrounds(True)
                for ground in grounds:
                    result = self._buildGroundNode(ground)
                    if result:
                        yield result
                    else:
                        devices = IOT.getDevices(ground['id'])
                        for device in devices:
                            result = self._buildDeviceNode(device, node)
                            if result:
                                yield result
                            else:
                                assets = IOT.getAssets(device['id'])
                                for asset in assets:
                                    result = self._buildAssetNode(asset, node)
                                    if result:
                                        yield result
            elif hasattr(node, 'ground_id'):
                devices = IOT.getDevices(node.ground_id)
                for device in devices:
                    result = self._buildDeviceNode(device, node)
                    if result:
                        yield result
                    else:
                        assets = IOT.getAssets(device['id'])
                        for asset in assets:
                            result = self._buildAssetNode(asset, node)
                            if result:
                                yield result
            elif hasattr(node, 'device_id'):
                assets = IOT.getAssets(node.device_id)
                for asset in assets:
                    result = self._buildAssetNode(asset, node)
                    if result:
                        yield result
        except Exception as e:
            showError(e)

    def _buildGroundNode(self, ground):
        if self.create_node_func:
            result = self.create_node_func(ground, 'ground')
        else:
            result = TreeViewLabel(text=ground['title'], )
        if result:
            result.is_open = False
            result.is_leaf = False
            result.no_selection = True
            result.ground_id = ground['id']
            return result

    def _buildDeviceNode(self, device, node):
        if self.create_node_func:
            result = self.create_node_func(device, 'device', node)
        else:
            result = TreeViewLabel()
            if device['title']:
                result.text = device['title']  # for old devices that didn't ahve a title yet.
            else:
                result.text = device['name']
        if result:
            result.is_open = False
            result.is_leaf = False
            result.no_selection = True
            result.device_id = device['id']
            return result

    def _buildAssetNode(self, asset, node):
        if self.create_node_func:
            result = self.create_node_func(asset, 'asset', node)
        else:
            result = TreeViewLabel()
            if asset['title']:
                result.text = asset['title']  # for old devices that didn't ahve a title yet.
            else:
                result.text = asset['name']
        if result:
            result.is_open = False
            result.is_leaf = True
            result.asset_id = asset['id']
            return result