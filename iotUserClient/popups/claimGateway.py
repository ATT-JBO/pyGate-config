__author__ = 'Jan Bogaerts'
__copyright__ = "Copyright 2016, AllThingsTalk"
__credits__ = []
__maintainer__ = "Jan Bogaerts"
__email__ = "jb@allthingstalk.com"
__status__ = "Prototype"  # "Development", or "Production"

import kivy

from kivy.uix.popup import Popup
from kivy.properties import StringProperty, NumericProperty
from kivy.lang import Builder
from kivy.clock import Clock

import iotUserClient.attiotuserclient as IOT

Builder.load_string("""
<ClaimGatewayDialog>:

    auto_dismiss: False
    title: 'Claim gateway'
    size_hint: None, None
    width: '300dp'
    height:  grdMain.minimum_height + dp(60) # '440dp'
    pos_hint:{'center_x': .5, 'center_y': .5}
    GridLayout:
        id: grdMain
        rows: 3
        label:
            text: 'Searching for gateway...'
            size_hint_y: None
            height:'32dp'
        label:
            text: str(root.count)
            size_hint_y: None
            height:'32dp'
        Button:
            text: 'Cancel'
            on_press: root.cancel()
            size_hint_y: None
            height:'32dp'
""")

class ClaimGatewayDialog(Popup):
    "set credentials"
    count = NumericProperty(30)
    def __init__(self, callback = None, **kwargs):
        self.callback = callback
        super(ClaimGatewayDialog, self).__init__(**kwargs)

    def claim(self, groundId, claimCode):
        self.groundId = groundId
        self.claimCode = claimCode
        result = IOT.sendClaim(self.groundId, self.claimCode)
        if not result:
            self.open()
            Clock.schedule_interval(self.on_clock, 1)
        elif self.callback:
            self.callback(result)
        return result

    def on_clock(self, dt):
        if self.count == 0:
            self.message = "claim failed"
            self.buttonLabel = 'Done'
            return False
        else:
            result = IOT.sendClaim(self.groundId, self.claimCode)
            if result:
                self.dismissOk()
                return False
            self.count -= 1
            return True

    def dismissOk(self):
        if self.callback:
            self.callback(self.gateway)
        self.dismiss()

    def cancel(self):
        self.dismiss()