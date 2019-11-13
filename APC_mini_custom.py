from __future__ import absolute_import, print_function, unicode_literals
import Live
from functools import partial
from itertools import izip

import Live
import sys

from _Framework.Layer import Layer
from _Framework.TransportComponent import TransportComponent
from _Framework.ButtonMatrixElement import ButtonMatrixElement

from _APC.APC import APC
from _APC.ControlElementUtils import make_button, make_pedal_button, make_slider

import APC_mini_custom.display as disp
import APC_mini_custom.skins as skins
from APC_mini_custom.CueComponent import CueComponent

MATRIX_SIZE = 8
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

    def really_send_midi(self, midi_bytes):
        super(APC_mini_custom, self)._do_send_midi(midi_bytes)

    # Setting up
    def __init__(self, *a, **k):
        super(APC_mini_custom, self).__init__( *a, **k)
        disp.clearAll(self)
        #disp.splash(self)
        self.print_message("Initialized APC")
        self._skin = skins.make_skin()
        self._suppress_send_midi = False
        with self.component_guard():
            self.setup()   


    def setup(self):
        self.setupStarted = True
        self._create_controls()
        self._setup_cue_control()
        self._setup_transport_control()

    def _create_controls(self):
        make_color_button = partial(make_button, skin=self._skin)
        self._matrix_buttons = [ make_color_button(0, i, name=b'Matrix_Button_%d' % i ) for i in range(MATRIX_SIZE*MATRIX_SIZE) ]
        cue_rows = 3
        self._cue_buttons = [ self._matrix_buttons[i] for r in range(cue_rows) for i in range(MATRIX_SIZE*(MATRIX_SIZE-(r+1)),MATRIX_SIZE*(MATRIX_SIZE-r)) ]
        for button in self._cue_buttons:
            button._skin = skins.get_cue_button()
        
        self._vertical_buttons = [ make_color_button(0, 82 + i, name="Vertical_Button_%d" % i ) for i in range(MATRIX_SIZE) ]
        self._horizontal_buttons = [ make_color_button(0, 64 + i, name="Horizontal_Button_%d" % i ) for i in range(MATRIX_SIZE) ]

        self._left_button = self._horizontal_buttons[2]
        self._right_button = self._horizontal_buttons[3]

    def _setup_cue_control(self):
        self._cue_control = CueComponent(self, name=b'Cue_Point_Control', play_on_cue=True)
        self._cue_control.set_cue_buttons(self._cue_buttons)
        self._cue_control.set_enabled(True)
        cuepoints = self.song().cue_points
        self.print_message(str(cuepoints[0].name))
        self.song().cue_points[3].jump()
 
    def _setup_transport_control(self):
        self._transport_control = TransportComponent(name=b'Transport')
        #self._transport_control.set_play_button(self._matrix_buttons[0])
        self._transport_control.set_enabled(True)