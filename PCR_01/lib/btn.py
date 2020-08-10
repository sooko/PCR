from kivy.uix.behaviors.touchripple import  TouchRippleButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior,ToggleButtonBehavior
from kivy.lang import  Builder
Builder.load_string("""

""")

class Btn(TouchRippleButtonBehavior,Label):
    pass
class BtnImg(TouchRippleButtonBehavior,Image):
    pass
class ButtonImg(ButtonBehavior,Image):
    pass
class ToggleButtonImg(ToggleButtonBehavior,Image):
    pass
class BtnPush(ButtonImg):
    pass
