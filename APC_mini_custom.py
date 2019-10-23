#Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/APC_mini/APC_mini.py
from __future__ import with_statement
from _Framework.Layer import Layer, SimpleLayerOwner
from _APC.ControlElementUtils import make_slider
from _Framework.ControlSurface import ControlSurface
from _APC.APC import APC
from APC_Key_25.APC_Key_25 import APC_Key_25
from APC_mini.APC_mini import APC_mini
import time
import display as disp

NOTE_ON_STATUS = 144
NOTE_OFF_STATUS = 128
SHIFT = 98
CC_STATUS = 176

class APC_mini_custom(APC):
    def __init__(self, *a, **k):
        super(APC_mini_custom, self).__init__( *a, **k)

    def _product_model_id_byte(self):
        return 40

# Base class for a mode
class Mode():
    def __init__(self, apc):
        self.apc = apc

# Ableton Control mode
class AbletonControls(Mode):
    def __init__(self, apc):
        Mode.__init__(self, apc)

# Track Arm mode
class TrackArm(Mode):
    def __init__(self, apc):
        Mode.__init__(self, apc)
        apc.create_arm_buttons()

# Setlist mode
class Setlist(Mode):
    def __init__(self, apc):
        Mode.__init__(self, apc)