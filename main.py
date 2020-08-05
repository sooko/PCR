from kivy.utils import platform
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'width', 1024)
Config.set('graphics', 'height', 600)

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty, DictProperty, ListProperty, ObjectProperty
import json
from kivy.storage.jsonstore import JsonStore
Builder.load_file('kv/ml.kv')
Builder.load_file('kv/topnav.kv')
Builder.load_file('kv/sc1.kv')
Builder.load_file('kv/sc2.kv')
Builder.load_file('kv/sc3.kv')
Builder.load_file('kv/sc4.kv')
Builder.load_file('kv/home.kv')
from kivy.clock import Clock
from btn import *
class Sc1(Screen):
    param=ListProperty([0,0,0,0,0,0,0,0,0])
    btns_state=DictProperty({})
    def __init__(self,*args,**kwargs):
        self.register_event_type("on_set")
        super(Sc1,self).__init__(*args,**kwargs)
        Clock.schedule_once(self.delay,1)
    def delay(self,dt):
        try:
            f=open("btnstate.json","r")
            self.btns_state=json.load(f)
            f.close()
            for i in self.ids.gridsave.children:
                i.alpa=self.btns_state[i.text]
            f=open("curent_protokol.json","r")
            self.param=json.load(f)["curent_protokol"]
            self.dispatch("on_set")
        except:
            pass
    def on_set(self):
        self.d={"curent_protokol":self.param}
        f=open("curent_protokol.json","w")
        json.dump(self.d,f)
        f.close()
    def save(self,a):
        self.d={a:self.param}
        f=open("protokol{}.json".format(a),"w")
        json.dump(self.d,f)
        f.close()
        self.save_state()
    def load(self,a,b):
        if a==1:
            f=open("protokol{}.json".format(b),"r")
            self.param=json.load(f)[b]
            f.close()
        else:
            print("no data")
    def save_state(self):
        for i in self.ids.gridsave.children:
            self.btns_state[i.text]=i.alpa
        f=open("btnstate.json","w")
        json.dump(self.btns_state,f)
        f.close()
class Sc2(Screen):
    list_plate=ListProperty([0,0,0,0,0])
    btns_state=DictProperty({})
    def __init__(self,*args,**kwargs):
        self.register_event_type("on_set")
        super(Sc2,self).__init__(*args,**kwargs)
        Clock.schedule_once(self.delay,1)
    def delay(self,dt):
        try:
            f=open("btnstate1.json","r")
            self.btns_state=json.load(f)
            f.close()
            # print(self.btns_state)
            for i in self.ids.gridsave.children:
                i.alpa=self.btns_state[i.text]
            f=open("curent_plate.json","r")
            self.list_plate=json.load(f)["curent_plate"]
            self.dispatch("on_set")
        except:
            pass
    def on_set(self):
        self.d={"curent_plate":self.list_plate}
        f=open("curent_plate.json","w")
        json.dump(self.d,f)
        f.close()

    def save(self,a):
        self.d={a:self.list_plate}
        f=open("plate{}.json".format(a),"w")
        json.dump(self.d,f)
        f.close()
        self.save_state()
    def load(self,a,b):
        if a==1:
            f=open("plate{}.json".format(b),"r")
            self.list_plate=json.load(f)[b]
            f.close()
        else:
            print("no data")
    def save_state(self):
        for i in self.ids.gridsave.children:
            self.btns_state[i.text]=i.alpa
        f=open("btnstate1.json","w")
        json.dump(self.btns_state,f)
        f.close()
class Home(Screen):
    protokol=ListProperty([0,0,0,0,0,0,0,0,0])
    plate=ListProperty([0,0,0,0,0])
    detik=NumericProperty(0)
    menit=NumericProperty(0)
    waktu=StringProperty("00:00:00")
    temp=NumericProperty(0)
    cycles=NumericProperty(0)
    def __init__(self,*args,**kwargs):
        super(Home,self).__init__(*args,**kwargs)


class Ml(FloatLayout):
    protokol=ListProperty([0,0,0,0,0,0,0,0,0])
    plate=ListProperty([0,0,0,0,0])
    def __init__(self,*args,**kwargs):
        super(Ml,self).__init__(*args,**kwargs)
    def set_protokol(self,a):
        self.protokol=a
    def on_protokol(self,a,b):
        print(b)
    def set_plate(self,a):
        self.plate=a
    def on_plate(self,a,b):
        print(b)
class SmartPcr(App):
    ml=Ml()
    def build(self):
        return self.ml
if __name__=="__main__":
    SmartPcr().run()
