from kivy.utils import platform
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'width', 1024)
Config.set('graphics', 'height', 600)
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty, DictProperty, ListProperty, ObjectProperty
Builder.load_file('kv/ml.kv')
Builder.load_file('kv/topnav.kv')
Builder.load_file('kv/sc1.kv')
Builder.load_file('kv/sc2.kv')
Builder.load_file('kv/sc3.kv')
Builder.load_file('kv/sc4.kv')
Builder.load_file('kv/home.kv')

from btn import *
class Sc1(Screen):
    param=ListProperty([0,0,0,0,0,0,0,0,0])
    def __init__(self,*args,**kwargs):
        self.register_event_type("on_set")
        super(Sc1,self).__init__(*args,**kwargs)
    def on_set(self):
        # print("set")
        pass
class Sc2(Screen):
    param=ListProperty([0,0,0,0,0])
    def __init__(self,*args,**kwargs):
        super(Sc2,self).__init__(*args,**kwargs)
class Home(Screen):
    protokol=ListProperty([0,0,0,0,0,0,0,0,0])
    
    def __init__(self,*args,**kwargs):
        super(Home,self).__init__(*args,**kwargs)

# class Sc2(Screen):
#     param=ListProperty([0,0,0,0,0])
#     def __init__(self,*args,**kwargs):
#         super(Sc2,self).__init__(*args,**kwargs)

class Ml(FloatLayout):
    protokol=ListProperty([0,0,0,0,0,0,0,0,0])
    def __init__(self,*args,**kwargs):
        super(Ml,self).__init__(*args,**kwargs)
    def set_protokol(self,a):
        self.protokol=a
    def on_protokol(self,a,b):
        print(b)

    
class SmartPcr(App):
    ml=Ml()
    def build(self):
        return self.ml

if __name__=="__main__":
    SmartPcr().run()