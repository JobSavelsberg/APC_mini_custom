
#Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/APC_mini/__init__.py
from _Framework.Capabilities import CONTROLLER_ID_KEY, PORTS_KEY, NOTES_CC, SCRIPT, REMOTE, controller_id, inport, outport
from APC_mini_custom import APC_mini_custom

def create_instance(c_instance):
    return APC_mini_custom(c_instance)


def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=2536, product_ids=[40], model_name='APC MINI CUSTOM'),
     PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT, REMOTE]), outport(props=[SCRIPT, REMOTE])]}