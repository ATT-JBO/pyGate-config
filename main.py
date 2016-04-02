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

from iotUserClient.popups.credentials import CredentialsDialog
import iotUserClient.attiotuserclient as IOT
from errors import *
import gateway


class MainWindow(Widget):
    def __init__(self, **kwargs):
        self.data = None
        super(MainWindow, self).__init__(**kwargs)

    def editCredentials(self):
        dlg = CredentialsDialog(gateway.data.credentials, self._credentialsChanged)
        dlg.open()

    def _credentialsChanged(self, newvalue):
        IOT.disconnect(False)
        gateway.data.credentials = newvalue
        popup = Popup(title='connecting', content=Label(text='searching for gateways,\nand syncing...'),
                      size_hint=(None, None), size=(400, 250), auto_dismiss=False)
        popup.bind(on_open=self._syncWithCloud)
        popup.open()

    def _syncWithCloud(self, instance):
        try:
            Application.connect()
            gateway.data.scanGrounds()
        finally:
            instance.dismiss()


class homeConfigApp(App):
    def build(self):
        gateway.data.loadSettings()
        self.connect()
        self._main = MainWindow()
        return self._main

    def on_pause(self):                         # can get called multiple times, sometimes no memory objects are set
        self.saveState(True)
        return True

    def on_resume(self):
        try:
            if gateway.data.credentials.isDefined():                            # can get called multiple times, sometimes no memory objects are set
                IOT.reconnect(gateway.data.credentials.server, gateway.data.credentials.broker)
                logging.info("reconnected after resume")
        except Exception as e:
            showError(e)

    def on_stop(self):
        self.saveState(False)


    def saveState(self, recoverable):
        '''close the connection, save the settings.'''
        try:
            #data.saveSettings() not required, already done after changing the settings.
            IOT.disconnect(recoverable)                        # close network connection, for cleanup
        except:
            logging.exception('failed to save application state')


Application = homeConfigApp()

if __name__ == '__main__':
    try:
        Application.run()
    except Exception as e:
        showError(e, "fatal error")