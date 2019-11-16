from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot, subject_slot_group
from _Framework.CompoundComponent import CompoundComponent
from _Framework.DeviceComponent import DeviceComponent



class CueComponent(ControlSurfaceComponent):
    
    _cue_buttons = []
    _instrument_buttons = []
    _prev_cue_button = None
    _next_cue_button = None
    _current_song_index = 0
    _current_instrument_index = 0
    _play_on_cue = True
    _cues = []
    _song_cues = []
    _instrument_cues = []
    _midiccinst_params = []
    _midiccinst_prevval = []

    _instrument_button_setup_done = False

    def __init__(self, apc, play_on_cue, *a, **k):
        super(CueComponent, self).__init__(*a, **k)
        self._play_on_cue = play_on_cue
        self._on_can_jump_to_prev_cue_changed.subject = self.song()
        self._on_can_jump_to_next_cue_changed.subject = self.song()

        self.apc = apc
    
    def _on_midiccinst_change(self):
        if(self._instrument_button_setup_done):
            for i, param in enumerate(self._midiccinst_params):
                if(param.value != self._midiccinst_prevval[i]):
                    self._current_instrument_index = i
                    self._midiccinst_prevval[i] = param.value
            self._instrument_cues[self._current_song_index][self._current_instrument_index].jump()
            self.update_buttons()

    def set_cue_buttons(self, buttons):
        self._cues = sorted(self.song().cue_points, key=lambda cue: cue.time)

        instrument_index = 0
        for cue in self._cues:
            if(cue.name[0] != '_'): 
                self._song_cues.append(cue)
                instrument_index+=1
                self._instrument_cues.append([])
            self._instrument_cues[instrument_index-1].append(cue)
        
        for i, button in enumerate(buttons):
            if(i < len(self._song_cues)):
                button.add_value_listener(self._on_select_cue_point, True)
                if(i % 3 == 0):
                    button.cue_color = "Amber"
                if(i % 3 == 1):
                    button.cue_color = "Green"
                if(i % 3 == 2):
                    button.cue_color = "Red"
                self._cue_buttons.append(button)
        self.update_buttons()

    def set_instrument_buttons(self, buttons):
        for i in range(min(5,len(buttons))):
            parameter = self.song().tracks[0].devices[0].parameters[2+i*2]
            parameter.add_value_listener(self._on_midiccinst_change)
            self._midiccinst_params.append(parameter)
            self._midiccinst_prevval.append(parameter.value)
            

        for button in buttons:
            button.add_value_listener(self._on_select_instrument, True)
            self._instrument_buttons.append(button)
        self.update_buttons()
        self._instrument_button_setup_done = True

    def set_prev_cue_button(self, button):
        self._prev_cue_button = button
        self._on_jump_to_prev_cue.subject = button
        self._on_can_jump_to_prev_cue_changed()

    @subject_slot(b'value')
    def _on_select_cue_point(self, value, sender):
        index = self._cue_buttons.index(sender)
        if( value > 0):
            #self.song().is_playing = self._play_on_cue
            sender.set_light(sender.cue_color+"Cue.Disabled")
        else:
            #self.song().is_playing = False
            sender.set_light(sender.cue_color+"Cue.On")
        self._current_instrument_index = 0
        self._song_cues[index].jump()
        self._current_song_index = index
        self.update_buttons()
    
    @subject_slot(b'value')
    def _on_select_instrument(self, value, sender):
        index = self._instrument_buttons.index(sender)
        self._instrument_cues[self._current_song_index][index].jump()
        self._current_instrument_index = index
        self.update_buttons()

    @subject_slot(b'can_jump_to_prev_cue')
    def _on_can_jump_to_prev_cue_changed(self):
        if self._prev_cue_button != None:
            pass
            #self._prev_cue_button.set_light(self.song().can_jump_to_prev_cue)
        return

    @subject_slot(b'value')
    def _on_jump_to_prev_cue(self, value):
        if value or not self._prev_cue_button.is_momentary():
            if self.song().can_jump_to_prev_cue:
                self.song().jump_to_prev_cue()
                self._next_cue_button.set_light(False)
                self._prev_cue_button.set_light(True)

    def set_next_cue_button(self, button):
        self._next_cue_button = button
        self._on_jump_to_next_cue.subject = button
        self._on_can_jump_to_next_cue_changed()

    @subject_slot(b'can_jump_to_next_cue')
    def _on_can_jump_to_next_cue_changed(self):
        if self._next_cue_button != None:
            #self._next_cue_button.set_light(self.song().can_jump_to_next_cue)
            pass
        return

    @subject_slot(b'value')
    def _on_jump_to_next_cue(self, value):
        if value or not self._next_cue_button.is_momentary():
            if self.song().can_jump_to_next_cue:
                self.song().jump_to_next_cue()
                self._next_cue_button.set_light(True)
                self._prev_cue_button.set_light(False)


    def update_buttons(self):
        for i, song_button in enumerate(self._cue_buttons):
            if(i != self._current_song_index):
                song_button.set_light(song_button.cue_color+"Cue.Off")
            else:
                song_button.set_light(song_button.cue_color+"Cue.On")

        for i, instrument_button in enumerate(self._instrument_buttons):
            if( i < len(self._instrument_cues[self._current_song_index])):
                if ( i == self._current_instrument_index):
                    instrument_button.set_light("On")
                else:
                    instrument_button.set_light("Off")
            else:
                instrument_button.set_light("Disabled")

    def reset_lights(self):
        for button in self._cue_buttons:
            button.set_light(button.cue_color+"Cue.Disabled")
        for button in self._instrument_buttons:
            button.set_light("Disabled")
        self.update_buttons()
                
        
