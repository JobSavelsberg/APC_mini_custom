from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot, subject_slot_group
from _Framework.CompoundComponent import CompoundComponent

class CueComponent(ControlSurfaceComponent):
    
    _cue_buttons = []
    _prev_cue_button = None
    _next_cue_button = None
    _current_cue = None
    _play_on_cue = True

    def __init__(self, apc, play_on_cue, *a, **k):
        super(CueComponent, self).__init__(*a, **k)
        self._play_on_cue = play_on_cue
        self._on_can_jump_to_prev_cue_changed.subject = self.song()
        self._on_can_jump_to_next_cue_changed.subject = self.song()
        self.apc = apc
        

    def set_cue_buttons(self, buttons):
        for i, button in enumerate(buttons):
            self.apc.print_message("Button " + str(i) + ", "+ str(button.name))
            if(i < len(self.song().cue_points)):
                button.add_value_listener(self._on_select_cue_point, True)
                if(i % 3 == 0):
                    button.cue_color = "Amber"
                if(i % 3 == 1):
                    button.cue_color = "Green"
                if(i % 3 == 2):
                    button.cue_color = "Red"
                self._cue_buttons.append(button)
        self.update_cue_buttons()

    def set_prev_cue_button(self, button):
        self._prev_cue_button = button
        self._on_jump_to_prev_cue.subject = button
        self._on_can_jump_to_prev_cue_changed()

    @subject_slot(b'value')
    def _on_select_cue_point(self, value, sender):
        index = self._cue_buttons.index(sender)
        if( value > 0):
            self.song().is_playing = self._play_on_cue
            sender.set_light(sender.cue_color+"Cue.Disabled")
        else:
            self.song().is_playing = False
            sender.set_light(sender.cue_color+"Cue.On")
        self.song().cue_points[index].jump()
        self._current_cue = sender
        self.update_cue_buttons()

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


    def update_cue_buttons(self):
        self.apc.print_message("Updating cue buttons")
        for button in self._cue_buttons:
            if(button != self._current_cue):
                button.set_light(button.cue_color+"Cue.Off")
