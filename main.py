from kivy.utils import platform
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'width', 1024)
Config.set('graphics', 'height', 600)
from kivy.core.window import Window
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
from navigationdrawer import NavigationDrawer
from kivy.clock import Clock
from btn import *
from able import BluetoothDispatcher, GATT_SUCCESS,Advertisement
from kivy.core.audio import SoundLoader
sound=SoundLoader.load("sound/button-50.wav")
tit=SoundLoader.load("sound/beep-07.wav")
from xcamera import XCamera
# if platform=="android":
from jnius import autoclass
# from android.permissions import request_permissions, Permission
# request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
import os
class XCamera1(XCamera):
    pass
class BLE(BluetoothDispatcher):
    device = alert_characteristic = None
    state = StringProperty("not connect")
    notification_value = StringProperty('')
    uids = {
        'string': 'ffe1',
        'counter_reset': 'ffe1',
        'counter_increment': 'ffe1',
        'counter_read': 'ffe1',
        'notifications': 'ffe1'
    }
    def __init__(self, *args, **kwargs):
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
            self.write_characteristic(characteristic, self.data_out)
    def enab(self):
        self.enable_notifications(self.services.search('ffe1'))
    def on_characteristic_changed(self, characteristic):
        uuid = characteristic.getUuid().toString()
        if self.uids['notifications'] in uuid:
            value = characteristic.getStringValue(0)
            self.notification_value =str(value)
    def on_state(self,a,b):
        self.do_toast(b)
    def do_toast(self,b):
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        PythonActivity.toastError(b)
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
        sound.play()
    def do_toast(self,b):
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        PythonActivity.toastError(b)
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
        self.play_sound()
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
        sound.play()
    def do_toast(self,b):
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        PythonActivity.toastError(b)
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
    def __init__(self,*args,**kwargs):
        super(Home,self).__init__(*args,**kwargs)
        if platform=="android":
            self.ble=BLE()
            Clock.schedule_once(self.delay,1)
    def delay(self,dt):
        self.cam=XCamera1()
        self.ids.root_cam.add_widget(self.cam)
        self.cam.play = False
    def parsing_list(self,data):
        s=str(data)[1:-1]
        return s

    def play_sound(self):
        sound.play()
    def play_tit(self):
        tit.play()
    def on_state(self,a,b):
        if self.ble:
            if b==1:
                parser=self.parsing_list(self.protokol+self.plate)
                self.ble.data_out="*start,{}#\n".format(parser).encode()
                self.ble.start_alert()
                Clock.schedule_interval(self.timer,1)

            if b==0:
                self.ble.data_out="*finish#\n".encode()
                self.ble.start_alert()
                Clock.unschedule(self.timer)
                self.menit=0
                self.jam=0
                self.detik=0


    def timer(self,dt):
        self.detik+=1
        if self.detik==60:
            self.menit+=1
            self.play_tit()
            self.detik=0
        if self.menit==60:
            self.jam+=1
            self.menit=0
        self.waktu="{:02d}:{:02d}:{:02d}".format(self.jam,self.menit,self.detik)

    def do_toast(self,b):
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        PythonActivity.toastError(b)

class Ml(FloatLayout):
    protokol=ListProperty([0,0,0,0,0,0,0,0,0])
    plate=ListProperty([0,0,0,0,0])
    def __init__(self,*args,**kwargs):
        super(Ml,self).__init__(*args,**kwargs)

    #     Window.bind(on_keyboard=self.Android_back_click)

    # def Android_back_click(self,window,key,*largs):
    #     print(key)
    #     # if key == 27:
    #     #     self._scree_manager.current='screen1'#you can create a method here to cache in a list the number of screens and then pop the last visited screen.
    #     return True
    def set_protokol(self,a):
        self.protokol=a
    def on_protokol(self,a,b):
        pass
    def set_plate(self,a):
        self.plate=a
    def on_plate(self,a,b):
        # print(b)
        pass
class SmartPcr(App):
    ml=Ml()
    def build(self):
        return self.ml
if __name__=="__main__":
    SmartPcr().run()
