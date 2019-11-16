from __future__ import absolute_import, print_function, unicode_literals
import Live
from functools import partial
from itertools import izip

import Live
import sys

from _Framework.Layer import Layer
from _Framework.TransportComponent import TransportComponent
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.DeviceComponent import DeviceComponent

from _APC.APC import APC
from _APC.MixerComponent import MixerComponent
from _APC.ControlElementUtils import make_button, make_pedal_button, make_slider

import APC_mini_custom.display as disp
import APC_mini_custom.skins as skins
from APC_mini_custom.CueComponent import CueComponent
from APC_mini_custom.OmniComponent import OmniComponent

MATRIX_SIZE = 8
MIDI_NOTE_TYPE = 0
MIDI_CC_TYPE = 1
NOTE_ON_STATUS = 144
NOTE_OFF_STATUS = 128
SHIFT = 98
CC_STATUS = 176

mute = None

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
        #self.print_message("Sending " + str(midi_bytes))
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
        self.mute = self.song().master_track.devices[1].parameters[10]
        self._create_controls()
        self._cue_control = self._setup_cue_control()
        self._omni_control = self._setup_omni_control()
        self._master_controls = self._setup_master_controls()
        self._misc_controls = self._setup_misc_control()
        self._setup_transport_control()

    def _create_controls(self):
        make_color_button = partial(make_button, skin=self._skin)
        self._matrix_buttons = [ make_color_button(0, i, name=b'Matrix_Button_%d' % i ) for i in range(MATRIX_SIZE*MATRIX_SIZE) ]
        cue_rows = 3
        self._cue_buttons = [ self._matrix_buttons[i] for r in range(cue_rows) for i in range(MATRIX_SIZE*(MATRIX_SIZE-(r+1)),MATRIX_SIZE*(MATRIX_SIZE-r)) ]
        for button in self._cue_buttons:
            button._skin = skins.get_cue_button()
        self._instrument_buttons = [self._matrix_buttons[i] for i in range(MATRIX_SIZE-1)]
        for button in self._instrument_buttons:
            button._skin = skins.get_instrument_button()

        self._omni_buttons = [self._matrix_buttons[MATRIX_SIZE*3+i] for i in range(MATRIX_SIZE)]
        for button in self._omni_buttons:
            button._skin = skins.get_omni_button()
        self._vertical_buttons = [ make_color_button(0, 82 + i, name="Vertical_Button_%d" % i ) for i in range(MATRIX_SIZE) ]
        self._horizontal_buttons = [ make_color_button(0, 64 + i, name="Horizontal_Button_%d" % i ) for i in range(MATRIX_SIZE) ]

        self._left_button = self._horizontal_buttons[2]
        self._right_button = self._horizontal_buttons[3]

        self._master_add_volume_control = make_slider(0, 55, name=b'Master_Add_Volume_Control')
        self._master_sub_volume_control = make_slider(0, 56, name=b'Master_Sub_Volume_Control')
        self._master_mute_control = self._horizontal_buttons[7]
        self._master_mute_control._skin = skins.get_mute_button()

        self._splash_button = self._vertical_buttons[0]

    def _setup_cue_control(self):
        cue_control = CueComponent(self, name=b'Cue_Point_Control', play_on_cue=True)
        cue_control.set_cue_buttons(self._cue_buttons)
        cue_control.set_instrument_buttons(self._instrument_buttons)
        cue_control.set_enabled(True)
        return cue_control
 
    def _setup_omni_control(self):
        omni_control = OmniComponent(self, name=b"Omni_Control")
        omni_control.set_buttons(self._omni_buttons)
        omni_control.set_enabled(True)
        return omni_control

    def _setup_master_controls(self):
        self._master_mute_control.add_value_listener(self._on_master_mute_changed)
        return self._master_mute_control
    def _on_master_mute_changed(self, value):
        if(value>0):
            if(self.mute.value<.5):
                self.mute.value = 1
                self._master_mute_control.set_light("On")
            else:
                self.mute.value = 0
                self._master_mute_control.set_light("Off")

    def _setup_misc_control(self):
        self._splash_button.add_value_listener(self._on_splash)
        self.splashing = False
        return self._splash_button
    def _on_splash(self, value):
        if(value>0):
            if(self.splashing):
                self.splashing = False
                disp.clearAll(self)
                self._cue_control.reset_lights()
            else:
                self.splashing = True
                disp.splash(self)

    def _setup_transport_control(self):
        self._transport_control = TransportComponent(name=b'Transport')
        self._transport_control.set_enabled(True)