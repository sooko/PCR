import os
from kivy.utils import platform
from jnius import autoclass
if platform=="android":
    from jnius import autoclass
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
    try:
        os.mkdir("/storage/emulated/0/DCIM/PCR")
    except:
        pass
from clr import rgb_clr
from xcamera import XCamera
from kivy.config import Config
Config.set('graphics', 'width', 1024)
Config.set('graphics', 'height', 600)
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from lib.navigationdrawer import *
from lib.btn import *
from lib.ble import *
from kivy.app import App
Builder.load_file("kv/ml.kv")
Builder.load_file("kv/sc1.kv")
Builder.load_file("kv/sc2.kv")
Builder.load_file("kv/material.kv")
Builder.load_file("kv/topnav.kv")
from kivy.properties import NumericProperty,StringProperty,ListProperty,DictProperty
from kivy.uix.screenmanager import Screen,ScreenManager
import json
from kivy.clock import Clock
from binascii import hexlify,unhexlify
from struct import unpack,pack
import time
from kivy.metrics import dp,sp
class Ml(FloatLayout):
    war=StringProperty("")
    protokol=ListProperty([0,0,0,0,0,0,0,0,0]) 
    plate=ListProperty([0,0,0,0,0])
    detik=NumericProperty(0)
    menit=NumericProperty(0)
    jam=NumericProperty(0)
    temp=NumericProperty(0)
    cycles=NumericProperty(0)
    step=NumericProperty(0)
    state=NumericProperty(0)
    cam=None
    ble=None
    def __init__(self,*args,**kwargs):
        super(Ml,self).__init__(*args,**kwargs)
        if platform=="android":
            self.ble=BLE()
            self.ble.on_data_masuk=self.on_data_masuk
    def print_cam(self,a):
        pass
    def set_warna(self,dt,b):
        self.ids.line.size=b
        self.ids.bunder.warna=(dt[0]/255,dt[1]/255,dt[2]/255,dt[3]/255)
        tup=(dt[0],dt[1],dt[2])
        # if tup in rgb_clr.keys():
        #     for i in rgb_clr.
        #     if tup[0] in range(tup[0]-10,tup[0]+10):
        #         print(rgb_clr[tup])
        for i in rgb_clr.keys():
            if i[0] in range(tup[0]-15,tup[0]+15) and i[1] in range(tup[1]-15,tup[1]+15) and i[2] in range(tup[2]-15,tup[2]+15) :
                self.war=rgb_clr[i][0]
        self.ids.lbl_clr.text=self.war

            


    def update(self,dt):
        print(self.ids.cam.texture.pixels)
    def on_data_masuk(self):
        arr=unhexlify(self.ble.notification_value)
        un=unpack(">HBBB",arr)
        self.temp=un[0]/10
        self.step=un[1]
        self.cycles=un[3]
    def on_step(self,a,b):
        if b!=0:
            for i in self.ids.root_step.children:
                i.ambeyen=0
            self.ids.root_step.children[4-b].ambeyen=.9
        if b==0:
            self.do_toast("heating")
    def parsing_list(self,data):
        a=str(data)[1:-1].replace(" ","")
        return a
    def on_state(self,a,b):
        if self.ble:
            if b==1:
                parser=self.parsing_list(self.protokol+self.plate)
                data_out="*start,{}#".format(parser)
                for i in data_out:
                    if i!=" ":
                        self.ble.write(i.encode())
                        time.sleep(.01)
                time.sleep(.01)
                self.ble.write("\r\n".encode())
                Clock.unschedule(self.timer)
                Clock.schedule_interval(self.timer,1)
            elif b==0:
                data_out="*finish#\r\n"
                self.ble.write(data_out.encode())
                Clock.unschedule(self.timer)
                self.menit=0
                self.jam=0
                self.detik=0
    def do_toast(self,b):
        pass
    def timer(self,dt):
        self.detik+=1
        if self.detik==60:
            self.menit+=1
            self.detik=0
        if self.menit==60:
            self.jam+=1
            self.menit=0
        self.waktu="{:02d}:{:02d}:{:02d}".format(self.jam,self.menit,self.detik)
class Sc1(Screen):
    protokol=ListProperty([0,0,0,0,0,0,0,0,0])
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
class Sc2(Screen):
    plate=ListProperty([0,0,0,0,0])
    btns_state=DictProperty({})
    def __init__(self,*args,**kwargs):
        self.register_event_type("on_set")
        super(Sc2,self).__init__(*args,**kwargs)
        Clock.schedule_once(self.delay,1)
    def delay(self,dt):
        try:
            f=open("storages/btnstate1.json","r")
            self.btns_state=json.load(f)
            f.close()
            for i in self.ids.gridsave.children:
                i.alpa=self.btns_state[i.text]
            f=open("storages/curent_plate.json","r")
            self.plate=json.load(f)["curent_plate"]
            self.dispatch("on_set")
        except:
            pass
    def on_set(self):
        self.d={"curent_plate":self.plate}
        f=open("storages/curent_plate.json","w")
        json.dump(self.d,f)
        f.close()
    def save(self,a):
        self.d={a:self.plate}
        f=open("storages/plate{}.json".format(a),"w")
        json.dump(self.d,f)
        f.close()
        self.save_state()
    def load(self,a,b):
        if a==1:
            f=open("storages/plate{}.json".format(b),"r")
            self.plate=json.load(f)[b]
            f.close()
        else:
            self.do_toast("no data loaded")
    def save_state(self):
        for i in self.ids.gridsave.children:
            self.btns_state[i.text]=i.alpa
        f=open("storages/btnstate1.json","w")
        json.dump(self.btns_state,f)
        f.close()
    def do_toast(self,b):
        pass
class PCR(App):
    def build(self):
        return Ml()
if __name__=="__main__":
    PCR().run()
    