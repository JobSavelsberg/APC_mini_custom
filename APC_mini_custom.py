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
import skins
from functools import partial

from _APC.SkinDefault import make_default_skin, make_biled_skin, make_stop_button_skin
from _Framework.ButtonElement import ButtonElement
from _Framework.TransportComponent import TransportComponent
from _Framework.ToggleComponent import ToggleComponent

from _APC.ControlElementUtils import make_button, make_knob

MIDI_NOTE_TYPE = 0
MIDI_CC_TYPE = 1
NOTE_ON_STATUS = 144
NOTE_OFF_STATUS = 128
SHIFT = 98
CC_STATUS = 176

class APC_mini_custom(APC):
    def _product_model_id_byte(self):
        return 40

    def __init__(self, *a, **k):
        super(APC_mini_custom, self).__init__( *a, **k)
        self.on_off_skin = skins.get_on_off()
        self._suppress_send_midi = False
        self.setupStarted = False
        self.mode = AbletonControls(self)

    def setup(self):
        self.setupStarted = True
        self.show_message("Setting Up...")
        self.make_on_off_button = partial(make_button, skin=self.on_off_skin)
        self.mode.enter()


    def _on_identity_response(self, midi_bytes):
        super(APC_mini_custom, self)._on_identity_response(midi_bytes)
        self.setup()

    def _send_dongle_challenge(self):
        pass

    def _on_handshake_successful(self):
        pass

    def receive_midi(self, midi_bytes):
        self.log_message("Received: " + str(midi_bytes))
        self.show_message("Received: " + str(midi_bytes))
        super(APC_mini_custom, self).receive_midi(midi_bytes)


    # updates every 100 ms
    def update_display(self):
        super(APC_mini_custom, self).update_display()
        if (not self.setupStarted and not self._suppress_send_midi):
            self.splash()

    def splash(self):
        disp.img(self, disp.JOB)
        disp.allH(self, 1)
        disp.allV(self, 1)

    def _update_hardware(self):
        self._send_midi((240, 126, 127, 6, 1, 247))
        return
# Base class for a mode
class Mode():
    def __init__(self, apc):
        self.apc = apc
        self.apc.log_message("Mode set to: " + self.getName())
        self.apc.show_message("Mode set to: " + self.getName())

    def enter(self):
        self.apc.log_message("Entered mode: " + self.getName())
        self.apc.show_message("Entered mode: " + self.getName())
        disp.clearAll(self.apc)

# Mode Selector mode
class ModeSelector(Mode):
    def __init__(self, apc):
        Mode.__init__(self, apc)
    
    def getName(self):
        return "Mode Selector"

    def enter(self):
        Mode.enter(self)
        disp.allV(self.apc, 2)
        self.apc.log_message("Done entering")

# Ableton Control mode
class AbletonControls(Mode):
    def __init__(self, apc):
        Mode.__init__(self, apc)

    def getName(self):
        return "Ableton Controls"

    def enter(self):
        Mode.enter(self)

        self.transport = TransportComponent() #Instantiate a Transport Component
        self.transport.set_play_button(self.apc.make_on_off_button( 0, 0)) #ButtonElement(is_momentary, msg_type, channel, identifier)
        self.transport.set_stop_button(self.apc.make_on_off_button(0, 1))
        self.transport.set_record_button(self.apc.make_on_off_button(0, 2))
# Track Arm mode
class TrackArm(Mode):
    def __init__(self, apc):
        Mode.__init__(self, apc)
        apc.create_arm_buttons()

    def getName(self):
        return "Track Arm"
# Setlist mode
class Setlist(Mode):
    def __init__(self, apc):
        Mode.__init__(self, apc)

    def getName(self):
        return "Setlist"