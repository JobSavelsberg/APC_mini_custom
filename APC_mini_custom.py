#Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/APC_mini/APC_mini.py
from __future__ import with_statement
from _Framework.Layer import Layer, SimpleLayerOwner
from _APC.ControlElementUtils import make_slider
from APC_Key_25.APC_Key_25 import APC_Key_25
from APC_mini.APC_mini import APC_mini
import time
import display as disp

NOTE_ON_STATUS = 144
NOTE_OFF_STATUS = 128
SHIFT_KEY = 98
CC_STATUS = 176

class APC_mini_custom(APC_mini):
    SESSION_HEIGHT = 8
    HAS_TRANSPORT = False

    shiftPressed = False
    shiftPressedOnNoteKey = False
    lastNote = 0
    firstShiftClickedNote = -1
    lastShiftClickedNote = -1

    lastShiftUpMillis=0

    initialized = False

    def __init__(self, *a, **k):
        super(APC_mini_custom, self).__init__(*a, **k)
        self._suppress_session_highlight = True
        self.show_message("Initializing APC_mini_custom...")
        disp.clear(self)
        disp.img(self, disp.JOB)
        self.show_message("Initialized APC_mini_custom!")           
        self.initialized = True

    def _do_send_midi(self, midi_bytes):
        # Override so that when custom mode takes over none of the usual updates (e.g. mouse click on clip on Mac)
        # will cause changes to lights
        #return
        if(self.initialized):
            super(APC_mini_custom, self)._do_send_midi(midi_bytes)
        else:
            return


    # Used by edit modes to echo edit ops as lighting messages unrelated to usual Live clip events
    def really_do_send_midi(self, midi_bytes):
        super(APC_mini_custom, self)._do_send_midi(midi_bytes)

   
    def receive_midi(self, midi_bytes):
        song = self.song()

        self.show_message("Input: " + str(midi_bytes))
        if midi_bytes[0] & 240 == NOTE_ON_STATUS:
            note = midi_bytes[1]

            #song.create_midi_track()
            self.log_message("On: " + str(midi_bytes))
            self.log_message("Note: " + str(note))
            trackIndex = note%8
            self.arm_track(trackIndex)
            return            
        if midi_bytes[0] & 240 == NOTE_OFF_STATUS:
            note = midi_bytes[1]
            self.log_message("Off: " + str(midi_bytes))
            return
        super(APC_mini_custom, self).receive_midi(midi_bytes)

    def arm_track(self, trackIndex):
        song = self.song()
        track = song.tracks[trackIndex]
        if(track.can_be_armed):
            if(track.arm):
                track.arm = False
                disp.on(self, trackIndex, 0, 5)
            else:
                track.arm = True
                disp.on(self, trackIndex, 0, 3)

