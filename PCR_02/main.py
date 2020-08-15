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
from screens.screen1 import Sc1
from screens.screen2 import Sc2
from cam.xcamera import XCamera,LCamera
import threading
from lib.chart import Chart
from kivy.core.audio import SoundLoader

class Ml(FloatLayout):
    sound = SoundLoader.load('sound/telolet1.wav')
    war=StringProperty("")
    protokol=ListProperty([0,0,0,0,0,0,0,0,1])
    plate=ListProperty([0,0,0,0,0])
    detik=NumericProperty(0)
    menit=NumericProperty(0)
    jam=NumericProperty(0)
    temp=NumericProperty(0)
    cycles=NumericProperty(0)
    step=NumericProperty(0)
    state=NumericProperty(0)
    start=NumericProperty(0)
    flr=NumericProperty(0)
    camera_isready=BooleanProperty(False)
    cam=None
    ble=None
    loading_image=StringProperty("sooko.png")
    dict_step=DictProperty({0:"-",1:"RT",2:"PREDENAT",3:"DENAT",4:"ANNEAL",5:"CAPTURE"})
    def __init__(self,*args,**kwargs):
        super(Ml,self).__init__(*args,**kwargs)
        if platform=="android":
            self.ble=BLE()

            self.ble.on_data_masuk=self.on_data_masuk

            self.run_cam_thread()
        else:
            Clock.schedule_once(self.add_linuxcam,1)
    def run_cam_thread(self):
        if self.ble:
            data_out="*finish#\r\n"
            self.ble.write(data_out.encode())
            
        Clock.schedule_once(self.delay,5)
    def add_linuxcam(self,dt):
            self.lcam=LCamera(on_back=self.on_btn_camera_back)
            self.ids.root_cam.add_widget(self.lcam)
            self.lcam.pos_hint={"center_x":.5,"center_y":.5}
            self.lcam.play=False
            self.loading_image="img/white.png"
    def delay(self,dt):
        self.ids.root_cam.add_widget(XCamera(on_camera_ready=self.on_camera_ready))
        self.loading_image="img/white.png"
    def on_btn_camera_back(self,instance):
        if len(self.ids.root_cam.children)>0:
            if platform=="android":
                self.ids.root_cam.children[0].played=False
                light_off="*lightoff#\n".encode()
                if self.ble:
                    self.ble.write(light_off)
            else:
                self.ids.root_cam.children[0].play=False
        self.ids.main_manager.current="main_screen"
    def on_btn_set_camera_release(self):
        if len(self.ids.root_cam.children)>0:
            if platform=="android":
                if self.camera_isready:
                    self.ids.root_cam.children[0].played=True
                    self.ids.main_manager.current="cam_screen"
                    light_on="*lighton#\n".encode()
                    if self.ble:
                        self.ble.write(light_on)
                else:
                    self.do_toast("smart camera is not ready yet")
            else:
                self.ids.root_cam.children[0].play=True
                self.ids.main_manager.current="cam_screen"
    def on_camera_ready(self,instance):
        self.camera_isready=True
    def on_data_masuk(self):
        arr=unhexlify(self.ble.notification_value)
        un=unpack(">BHBBB",arr)
        print(un)
        self.start=un[0]
        self.temp=un[1]/10
        self.step=un[2]
        self.flr=un[4]
        self.cycles=un[4]
    def on_step(self,a,b):
        print(b)
        if b==5:
            self.ids.root_cam.children[0].shoot("{}".format(self.flr))
        if b in self.dict_step.keys():
            self.ids.display_step.value=self.dict_step[b]

    def on_cycles(self,a,b):
        if b==0:
            self.state=0
            self.sound.play()




            

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
        if platform=="android":
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            PythonActivity.toastError(b)
import sys
class PCR(App):
    def build(self):
        return Ml()
    def on_stop(self):
        sys.exit()
if __name__=="__main__":
    PCR().run()


