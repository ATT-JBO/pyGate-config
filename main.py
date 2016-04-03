__author__ = 'Jan Bogaerts'
__copyright__ = "Copyright 2016, AllThingsTalk"
__credits__ = []
__maintainer__ = "Jan Bogaerts"
__email__ = "jb@allthingstalk.com"
__status__ = "Prototype"  # "Development", or "Production"

import kivy
kivy.require('1.9.1')   # replace with your current kivy version !

import logging
logging.getLogger().setLevel(logging.INFO)

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.actionbar import ActionButton
from kivy.properties import ObjectProperty

from iotUserClient.popups.credentials import CredentialsDialog
import iotUserClient.attiotuserclient as IOT
from errors import *
import gateway
import data
import modules

class mainMenuActionButton(ActionButton):
    """shortcut for setting the same properties to all action buttons that represent modules."""
    def __init__(self, label, name, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.markup = True
        self.text = label
        self.key = name


class MainWindow(Widget):
    mainMenu = ObjectProperty()
    gatewaysMenu = ObjectProperty()
    screenMenu = ObjectProperty()
    screens = ObjectProperty()
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.loadGateways()
        self.loadScreens()
        self.loadActiveGateway()

    def loadScreens(self):
        """load all supported modules into the screen manager
        if the module is also supported by the gateway, then also add a button to the main menu
        """
        for key, module in modules.modules:
            try:
                if hasattr(module, 'getScreen'):
                    screen = module.getScreen()
                    if screen:
                        self.screens.add_widget(screen)
            except Exception as e:
                showError(e)
        self.loadViewFromSettings()

    def loadActiveGateway(self):
        """load the menu items for the current gateway and ask all required modules to update"""
        if data.currentGateway:
            childrenList = self.mainMenu.children
            self.mainMenu.clear_widgets(childrenList[:len(childrenList) - 2])   # remove all children except the last 2
            self.screenMenu.clear_widgets()
            for modname in data.currentGateway.modules:
                if modname in modules.modules:
                    module = modules.modules[modname]
                    if hasattr(module, 'getLabel'):
                        btn = mainMenuActionButton(module.getLabel(), modname)
                        btn.bind(on_press=self._navigateToModule)
                        self.mainMenu.add_widget(btn)
                screen = self.screens.get_screen(modname)
                if screen and hasattr(screen, 'updateData'):
                    screen.updateData()

    def loadGateways(self):
        """load all the gatewasy defined in the data object into the menu group so that the user can switch between gateways"""
        self.gatewaysMenu.clear_widgets()
        for gateway in data.gateways:
            btn = mainMenuActionButton(gateway.json['label'], gateway)
            btn.bind(on_press=self._setActiveGateway)
            self.mainMenu.add_widget(btn)

    def _setActiveGateway(self, instance):
        """called when a menu item is select to switch to a new gateway"""
        data.currentGateway = instance.key
        self.loadActiveGateway()

    def loadViewFromSettings(self):
        curView = data.getSetting('general', 'current view')
        if not curView:
            curView = 'gateways'
        self.screens.current = curView

    def _navigateToModule(self, instance):
        """called when a main menu item is selected.
        show the related screen"""
        try:
            if self.screens.current_screen and data.activeActionItems:
                self.screens.current_screen.actionItems = data.activeActionItems
                for item in data.activeActionItems:
                    self.mainMenu.remove_widget(item)
            self.screens.current = instance.key
            if self.screens.current_screen and self.screens.current_screen.actionItems:
                data.activeActionItems = self.screens.current_screen.actionItems
                for item in data.activeActionItems:
                    self.mainMenu.add_widget(item)
            else:
                data.activeActionItems = []
        except Exception as e:
            showError(e)

    def editCredentials(self):
        dlg = CredentialsDialog(gateway.data.credentials, self._credentialsChanged)
        dlg.open()

    def _credentialsChanged(self, newvalue):
        IOT.disconnect(False)
        data.credentials = newvalue
        popup = Popup(title='connecting', content=Label(text='searching for gateways,\nand syncing...'),
                      size_hint=(None, None), size=(400, 250), auto_dismiss=False)
        popup.bind(on_open=self._syncWithCloud)
        popup.open()

    def _syncWithCloud(self, instance):
        try:
            if data.credentials.isDefined():
                try:
                    Application.connect()
                    data.scanGrounds()
                    self.loadGateways()
                    #todo: show the gateway details
                except Exception as e:
                    showError(e)
        finally:
            instance.dismiss()


class homeConfigApp(App):
    def build(self):
        data.loadSettings()
        if data.credentials.isDefined():
            self.connect()
            data.scanGrounds()
        modules.load(data.moduleNames)
        self._main = MainWindow()
        return self._main

    def on_pause(self):                         # can get called multiple times, sometimes no memory objects are set
        self.saveState(True)
        return True

    def on_resume(self):
        try:
            if data.credentials.isDefined():                            # can get called multiple times, sometimes no memory objects are set
                IOT.reconnect(data.credentials.server, data.credentials.broker)
                logging.info("reconnected after resume")
        except Exception as e:
            showError(e)

    def on_stop(self):
        self.saveState(False)

    def connect(self):
        try:
            if data.credentials and data.credentials.isDefined():
                IOT.connect(data.credentials.userName, data.credentials.password, data.credentials.server, data.credentials.broker, data.credentials.secure)
                logging.info("reconnected after resume")
        except Exception as e:
            showError(e)

    def saveState(self, recoverable):
        '''close the connection, save the settings.'''
        try:
            data.saveSettings()
            IOT.disconnect(recoverable)                        # close network connection, for cleanup
        except:
            logging.exception('failed to save application state')


Application = homeConfigApp()

if __name__ == '__main__':
    try:
        Application.run()
    except Exception as e:
        showError(e, "fatal error")