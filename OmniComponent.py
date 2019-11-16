from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot, subject_slot_group



class OmniComponent(ControlSurfaceComponent):
    _buttons = []
    _omni_tracks = []

    def __init__(self, apc, *a, **k):
        super(OmniComponent, self).__init__(*a, **k)
        self.apc = apc
        for track in self.song().tracks:
            if(track.name.startswith("OMNI")):
                self._omni_tracks.append(track)

    def set_buttons(self, buttons):
        index = 0
        for button in buttons:
            if(index < len(self._omni_tracks)):
                index += 1
                self._buttons.append(button)
                button.add_value_listener(self.on_button_change, True)
                button.set_light("Off")

    def on_button_change(self, value, sender):
        index = self._buttons.index(sender)
        if(value > 0):
            if(self.toggle(index)):
                sender.set_light("On")
            else:
                sender.set_light("Off")

    def is_on(self, index):
        return self._omni_tracks[index].devices[0].parameters[0].value > 0

    def toggle(self, index):
        self._omni_tracks[index].devices[0].parameters[0].value = 0 if self.is_on(index) else 1
        return self.is_on(index)