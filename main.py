from kivy.uix.floatlayout import FloatLayout
from kivy.utils import platform
from kivy.lang import Builder
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
Builder.load_file('kv/home.kv')
from navigationdrawer import NavigationDrawer
from kivy.clock import Clock
from btn import *
import cv2
from able import BluetoothDispatcher, GATT_SUCCESS,Advertisement
import os
from xcamera import XCamera
if platform=="android":
    from jnius import autoclass
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
    try:
        os.mkdir("/storage/emulated/0/DCIM/PCR")
    except:
        pass
import threading
from struct import unpack
from binascii import hexlify,unhexlify
import time
class XCamera1(XCamera):
    pass
class BLE(BluetoothDispatcher):
    
    device = alert_characteristic = None
    state = StringProperty("not connect")
    notification_value = StringProperty('')
    karak=None
    uids = {
        'string': 'ffe1',
        'counter_reset': 'ffe1',
        'counter_increment': 'ffe1',
        'counter_read': 'ffe1',
        'notifications': 'ffe1'
    }
    def __init__(self, *args, **kwargs):
        self.register_event_type("on_data_masuk")
        super(BLE, self).__init__(**kwargs)
        self.data_out =bytearray([])
        self.start_alert()
    def start_alert(self, *args, **kwargs):
        if self.alert_characteristic:  
            self.alert(self.alert_characteristic)
        elif self.device:
            self.connect_gatt(self.device)
        else:
            self.stop_scan()
            self.start_scan()
    def on_device(self, device, rssi, advertisement):
        name = device.getName()
        if name and name.startswith(' = mantap'):  
            self.device = device
            self.stop_scan()
    def on_scan_completed(self):
        if self.device:
            self.connect_gatt(self.device)  
    def on_connection_state_change(self, status, state):
        if status == GATT_SUCCESS and state:  
            self.discover_services()  
            self.state = "terhubung"
        else:  
            self.alert_characteristic = None
            self.close_gatt()
            self.state = "sambungan gagal"
            self.start_alert()
    def on_services(self, status, services):
        self.alert_characteristic = services.search('ffe1')
        self.alert(self.alert_characteristic)
        self.services = services
        if self.state == "terhubung":
            self.enab()
    def alert(self, characteristic):
        if self.state == "terhubung":
            self.karak=characteristic
    def write(self,data):
        if self.state == "terhubung":
            if self.karak:
                self.write_characteristic(self.karak,data)
    def enab(self):
        self.enable_notifications(self.services.search('ffe1'))
    def on_characteristic_changed(self, characteristic):
        uuid = characteristic.getUuid().toString()
        if self.uids['notifications'] in uuid:
            value = characteristic.getStringValue(0)
            self.notification_value =str(value)
            # print(self.notification_value)
            self.dispatch("on_data_masuk")
    def on_state(self,a,b):
        self.do_toast(b)
    def do_toast(self,b):
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        PythonActivity.toastError(b)
    def on_data_masuk(self):
        pass
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
        self.play_sound()
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
    def play_sound(self):
        pass
    def do_toast(self,b):
        pass
        # PythonActivity = autoclass('org.kivy.android.PythonActivity')
        # PythonActivity.toastError(b)
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
            self.do_toast("no data loaded")
    def save_state(self):
        for i in self.ids.gridsave.children:
            self.btns_state[i.text]=i.alpa
        f=open("btnstate1.json","w")
        json.dump(self.btns_state,f)
        f.close()
    def play_sound(self):
        pass
    def do_toast(self,b):
        pass
class Home(Screen):
    protokol=ListProperty([0,0,0,0,0,0,0,0,0])
    plate=ListProperty([0,0,0,0,0])
    detik=NumericProperty(0)
    menit=NumericProperty(0)
    jam=NumericProperty(0)
    waktu=StringProperty("00:00:00")
    temp=NumericProperty(0)
    cycles=NumericProperty(0)
    ble=None
    state=NumericProperty(0)
    cam=None
    step=NumericProperty(0)
    def __init__(self,*args,**kwargs):
        self.register_event_type("on_setting_cam")
        self.register_event_type("on_step_run")
        super(Home,self).__init__(*args,**kwargs)
        if platform=="android":
            self.ble=BLE()
            self.ble.on_data_masuk=self.on_data_masuk
    def on_data_masuk(self):
        # print(self.ble.notification_value)
        
        arr=unhexlify(self.ble.notification_value)
        # print(arr)
        un=unpack(">HBBB",arr)
        print(un)
        self.temp=un[0]/10
        self.step=un[1]
        self.cycles=un[3]

        
        
    def on_step(self,a,b):
        if b!=0:
            for i in self.ids.root_step.children:
                i.ambeyen=0

            self.ids.root_step.children[4-b].ambeyen=.9
        self.dispatch("on_step_run")
    def on_step_run(self):
        pass
    def on_setting_cam(self):
        pass
    def parsing_list(self,data):
        s=str(data)[1:-1]
        return s
    def play_sound(self):
        pass
    def play_tit(self):
        pass
    def on_state(self,a,b):
        print(b)
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
    def timer(self,dt):
        self.detik+=1
        if self.detik==60:
            self.menit+=1
            self.detik=0
        if self.menit==60:
            self.jam+=1
            self.menit=0
        self.waktu="{:02d}:{:02d}:{:02d}".format(self.jam,self.menit,self.detik)
    def do_toast(self,b):
        pass
        # PythonActivity = autoclass('org.kivy.android.PythonActivity')
        # PythonActivity.toastError(b)
class Ml(FloatLayout):
    protokol=ListProperty([0,0,0,0,0,0,0,0,0])
    plate=ListProperty([0,0,0,0,0])
    def __init__(self,*args,**kwargs):
        super(Ml,self).__init__(*args,**kwargs)
        Clock.schedule_once(self.delay,3)
    def delay(self,dt):
        if platform=="android":
            self.ids.root_cam.add_widget(XCamera1())

    def set_protokol(self,a):
        self.protokol=a
    def on_protokol(self,a,b):
        pass
    def set_plate(self,a):
        self.plate=a
    def on_plate(self,a,b):
        pass
    def stop_cam(self):
        if len(self.ids.root_cam.children)>0:
            self.ids.root_cam.children[0].play=False
    def start_cam(self):
        if len(self.ids.root_cam.children)>0:
            self.ids.root_cam.children[0].play=True
        # if len(self.ids.cam.children)>0:
        #     self.ids.sc3.children[0].play=True
    def on_step_run(self,b):
        if b>2:
            self.start_cam()
        else:
            self.stop_cam()
class Sc3(Screen):
    pass
class SmartPcr(App):
    ml=Ml()
    def build(self):
        return self.ml
    # def on_pause(self):
    #     self.ml.stop_cam()
    #     return True
    # def on_resume(self):
    #     self.ml.start_cam()
if __name__=="__main__":
    SmartPcr().run()
    