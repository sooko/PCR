from kivy.properties import NumericProperty,StringProperty,ListProperty,DictProperty
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
import json
from kivy.lang import Builder
Builder.load_file("kv/sc1.kv")
class Sc1(Screen):
    protokol=ListProperty([0,0,0,0,0,0,0,0,1])
    btns_state=DictProperty({})
    def __init__(self,*args,**kwargs):
        self.register_event_type("on_set")
        super(Sc1,self).__init__(*args,**kwargs)
        Clock.schedule_once(self.delay,1)
    def delay(self,dt):
        try:
            f=open("storages/btnstate.json","r")
            self.btns_state=json.load(f)
            f.close()
            for i in self.ids.gridsave.children:
                i.alpa=self.btns_state[i.text]
            f=open("storages/curent_protokol.json","r")
            self.protokol=json.load(f)["curent_protokol"]
            self.dispatch("on_set")
        except:
            pass
    def on_set(self):
        self.d={"curent_protokol":self.protokol}
        f=open("storages/curent_protokol.json","w")
        json.dump(self.d,f)
        f.close()
    def save(self,a):
        self.d={a:self.protokol}
        f=open("storages/protokol{}.json".format(a),"w")
        json.dump(self.d,f)
        f.close()
        self.save_state()
    def load(self,a,b):
        if a==1:
            f=open("storages/protokol{}.json".format(b),"r")
            self.protokol=json.load(f)[b]
            f.close()
        else:
            print("no data")
    def save_state(self):
        for i in self.ids.gridsave.children:
            self.btns_state[i.text]=i.alpa
        f=open("storages/btnstate.json","w")
        json.dump(self.btns_state,f)
        f.close()
    def do_toast(self,b):
        pass
