from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Skin import Skin
from _Framework.ButtonElement import Color
from pushbase.colors import Rgb, Pulse, Blink
GREEN = Color(1)
GREEN_BLINK = Color(2)
RED = Color(3)
RED_BLINK = Color(4)
AMBER = Color(5)

class Defaults:
    class DefaultButton:
        On = Color(1)
        Off = Color(3)
        Disabled = Color(5)

def get_on_off():
    return Skin(Defaults)