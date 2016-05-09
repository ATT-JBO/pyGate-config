__author__ = 'Jan Bogaerts'
__copyright__ = "Copyright 2016, AllThingsTalk"
__credits__ = []
__maintainer__ = "Jan Bogaerts"
__email__ = "jb@allthingstalk.com"
__status__ = "Prototype"  # "Development", or "Production"

from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.uix.behaviors.drag import DragBehavior
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, BooleanProperty
from kivy.uix.treeview import TreeViewLabel
import json
import data

import iotUserClient.attiotuserclient as IOT

Builder.load_string("""
#:import AssetsTreeView iotUserClient.widgets.assetsTreeView.AssetsTreeView

<Actuator>:
    # Define the properties for the DragLabel
    drag_rectangle: self.x, self.y, self.width, self.height
    drag_timeout: 10000000
    drag_distance: 0
    Label:
        text: root.name
<Group>:
    assetsList: assetsLayout
    canvas.after:
        Line:
            rounded_rectangle: self.x,self.y,self.width,self.height, 8.0
    GridLayout:
        spacing: '8dp'
        size_hint: 1, None
        cols: 1
        TextInput:
            size_hint_y: None
            height:'32dp'
            write_tab: False
            hint_text: 'name of group'
            text: root.name
        TextInput:
            size_hint_y: None
            height:'32dp'
            write_tab: False
            hint_text: 'description'
            text: root.description
        TextInput:
            size_hint_y: None
            height:'32dp'
            write_tab: False
            hint_text: 'profile'
            text: root.profile
        TextInput:
            size_hint_y: None
            height:'32dp'
            write_tab: False
            hint_text: 'sleep time'
            text: root.sleep
        Label:
            size_hint_y: None
            height:'32dp'
            valign: 'bottom'
            text: '[b][u]actuators[/u][/b]'
            markup: True
        GridLayout:
            id: assetsLayout
            spacing: '8dp'
            size_hint: 1, None
            cols: 1
        Button:
            size_hint_y: None
            height:'32dp'
            text: 'add actuator'
            on_press: root.addActuator

<GroupsScreen>:
    GridLayout:
        rows: 2
        ScrollView:
            size_hint: 1, 1
            StackLayout:
                id: workspace_layout
                orientation: 'tb-lr'
                size_hint: 1, None
                pos_hint: {'x': 0, 'y': 0}
                padding: '10dp'
                spacing: '20dp'
                height: self.minimum_height
                BoxLayout:
                    spacing: '8dp'
                    size_hint: 1, None
                    height: '72dp'
                    orientation: 'vertical'
                    TextInput:
                        size_hint_y: None
                        height:'32dp'
                        write_tab: False
                        hint_text: 'name of group'
                    Button:
                        size_hint_y: None
                        height:'32dp'
                        text: 'add new group'
                        on_press: root.addGroup
        ScrollView:
            size_hint: 1, 1
            AssetsTreeView:
                hide_root: True
                indent_level: 4
                minimum_height: self.height
                create_node_func: root.createNode

""")

def getLabel():
    """return a label to represent the module. To include icons, use iconfonts.
    if this plugin does not have a screen, don't implement this function or return None.
    :rtype: basestring
    """
    return 'groups'

def getScreen():
    """returns the screen to show for editing this module's properties
    if this plugin does not have a view / screen, then return None or don't imlement this function.
    do the same for getLabel
    :rtype: Screen that has a function called 'updateData'. which is called whenever the currently active gateway is initially set / has changed
    """
    return GroupsScreen()

class GroupsScreen(Screen):
    def updateData(self):
        """update the data for the groups that should be displayed"""
        if data.currentGateway:
            fullDef = data.currentGateway.json
            groupDefs = [x for x in fullDef['devices'] if x['name'] == 'groups_groups']
            if len(groupDefs) > 0:
                groupDefs = groupDefs[0]                # the list selector always returns 1 element max, there is 1 device with that name.
                asset = [x for x in groupDefs['assets'] if x['name'] == 'groupDefs']
                if len(asset) > 0:
                    asset = asset[0]
                    self.groups = map(Group, asset['state']['value'])

    def createNode(self, obj, type, parent):
        if type == "device":
            if obj['gatewayId'] == data.currentGateway.json['id']:
                return TreeViewLabel(text=obj['title'])
        elif type == "asset":
            if parent:                  # if there is a parent, then the device was rendered, otherwise not device, so don't show.
                return TreeViewLabel(text=obj['title'])
        return None                     # we don't show grounds on this view, only the devices in this gateway


            #def addGroup(self, instance):


class Acuator(DragBehavior, Widget):
    name = StringProperty("")

    def loadData(self, assetId, parent):
        """load the name of the actuator and store the id."""
        self.asetId = assetId
        asset = IOT.getAsset(assetId)
        device = IOT.getDevice(asset['deviceId'])
        self.name = "{} on {}".format(asset['label'], device['label'])
        self.parent = parent

    def on_touch_up(self, touch):
        """when the user stops the drag this item out of the list, then remove it from the parent."""
        result = super(Acuator, self).on_touch_up(touch)
        self.parent.assetsList.remove_widget(self)
        return result


class Group(Widget):
    name = StringProperty("")
    description = StringProperty("")
    profile = StringProperty("")
    sleep = NumericProperty(0.1)        # nr of seconds between each actuator that gets triggered when the group is triggered
    assetsList = ObjectProperty()

    def __init__(self, data, **kwargs):
        super(Group, self).__init__(**kwargs)
        self.json = data
        if data:
            self.name = data['name']
            self.description = data['description']
            self.profile = json.dumps(data['profile'])
            self.sleep = data['sleep']
            self.actuators = data['actuators']
            for actuator in data['actuators']:
                item = Acuator()
                item.loadData(actuator, self)
                self.assetsList.add_widget(item)

    def addActuator(self, instance):
        """show the actuator selection box"""


