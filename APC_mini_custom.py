from __future__ import absolute_import, print_function, unicode_literals
import Live
from functools import partial
from itertools import izip

import Live
import sys

from _Framework.Layer import Layer

from _APC.APC import APC
from _APC.ControlElementUtils import make_button, make_pedal_button, make_slider

import APC_mini_custom.skins as skins
from APC_mini_custom.TestComponent import TestComponent

MIDI_NOTE_TYPE = 0
MIDI_CC_TYPE = 1
NOTE_ON_STATUS = 144
NOTE_OFF_STATUS = 128
SHIFT = 98
CC_STATUS = 176

class APC_mini_custom(APC):
    # Connecting APC to ableton
    def _product_model_id_byte(self):
        return 40
    
    def _update_hardware(self):
        self._send_midi((240, 126, 127, 6, 1, 247))
        return

    def _on_identity_response(self, midi_bytes):
        super(APC_mini_custom, self)._on_identity_response(midi_bytes)

    def _send_dongle_challenge(self):
        pass

    def _on_handshake_successful(self):
        pass

    def print_message(self, message):
        self.log_message(message)
        self.show_message(message)

    def receive_midi(self, midi_bytes):
        self.print_message("Received " + str(midi_bytes))
        super(APC_mini_custom, self).receive_midi(midi_bytes)

    # Setting up
    def __init__(self, *a, **k):
        super(APC_mini_custom, self).__init__( *a, **k)
        self.print_message("Initialized APC")
        with self.component_guard():
            self.setup()


    def setup(self):
        self.setupStarted = True
        self._create_controls()
        self._setup_cue_control()

    def _create_controls(self):
        #self._fader = make_slider(1, 48, b'Fader_%d' % 0)

        self._up_button = make_button(0, 64, b'Up_Button')
        self._down_button = make_button(0, 65, b'Down_Button')
        self._left_button = make_button( 0, 66, name = b'Left_Button')
        self._right_button = make_button( 0, 67, name = b'Right_Button')

    def _setup_cue_control(self):
        self._cue_control = TestComponent(self, name=b'Cue_Point_Control')
        self._cue_control.set_enabled(False)
        self._cue_control.layer = Layer(prev_cue_button=self._left_button, next_cue_button=self._right_button)
        self._cue_control.set_enabled(True)
        cuepoints = self.song().cue_points
        self.print_message(str(cuepoints[0].name))
        self.song().cue_points[3].jump()
