from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Skin import Skin
from _Framework.ButtonElement import Color
from pushbase.colors import Rgb, Pulse, Blink
OFF = Color(0)
GREEN = Color(1)
GREEN_BLINK = Color(2)
RED = Color(3)
RED_BLINK = Color(4)
AMBER = Color(5)
AMBER_BLINK = Color(6)

class Colors:
    class DefaultButton:
        On = GREEN
        Off = RED
        Disabled = OFF
    class Cue:
        class GreenCue:
            On = GREEN_BLINK
            Off = GREEN
            Disabled = OFF
        class RedCue:
            On = RED_BLINK
            Off = RED
            Disabled = OFF
        class AmberCue:
            On = AMBER_BLINK
            Off = AMBER
            Disabled = OFF
    class Instrument:
        On = GREEN
        Off = AMBER
        Disabled = OFF
    class Mute:
        On = RED
        Off = OFF
        Disabled = OFF
    class Omni:
        On = GREEN
        Off = AMBER
        Disabled = OFF

def make_skin():
    return Skin(Colors)
def get_cue_button():
    return Skin(Colors.Cue)
def get_instrument_button():
    return Skin(Colors.Instrument)
def get_mute_button():
    return Skin(Colors.Mute)
def get_omni_button():
    return Skin(Colors.Omni)