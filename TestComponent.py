from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot

class TestComponent(ControlSurfaceComponent):
    
    _prev_cue_button = None
    _next_cue_button = None

    def __init__(self, apc, *a, **k):
        super(TestComponent, self).__init__(*a, **k)
        self._on_can_jump_to_prev_cue_changed.subject = self.song()
        self._on_can_jump_to_next_cue_changed.subject = self.song()
        self.apc = apc

    def set_prev_cue_button(self, button):
        self._prev_cue_button = button
        self._on_jump_to_prev_cue.subject = button
        self._on_can_jump_to_prev_cue_changed()

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
                self.song().jump_to_prev_cue()[-lp]

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


