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
from lib.clr import rgb_clr
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
            Clock.schedule_once(self.delay,1)
        else:
            Clock.schedule_once(self.add_linuxcam,1)
    def add_linuxcam(self,dt):
            self.lcam=LCamera(on_back=self.on_btn_camera_back)
            self.ids.root_cam.add_widget(self.lcam)
            self.lcam.pos_hint={"center_x":.5,"center_y":.5}
            self.lcam.play=False
    def delay(self,dt):
        Clock.schedule_once(self.delay2,1)
    def delay2(self,dt):
        Clock.schedule_once(self.delay3,1)
    def delay3(self,dt):
        self.do_toast("preparing camera")
        self.ids.root_cam.add_widget(XCamera(on_camera_ready=self.on_camera_ready))
    def on_btn_camera_back(self,instance):
        if len(self.ids.root_cam.children)>0:
            if platform=="android":
                self.ids.root_cam.children[0].played=False
            else:
                self.ids.root_cam.children[0].play=False
        self.ids.main_manager.current="main_screen"
    def on_btn_set_camera_release(self):
        self.ids.main_manager.current="cam_screen"
        if len(self.ids.root_cam.children)>0:
            if platform!="android":
                self.ids.root_cam.children[0].play=True
            else:
                self.ids.root_cam.children[0].played=True
    def on_camera_ready(self,instance):
        self.do_toast("camera ready")
    def set_warna(self,dt,b):
        self.ids.line.size=b
        self.ids.bunder.warna=(dt[0]/255,dt[1]/255,dt[2]/255,dt[3]/255)
        tup=(dt[0],dt[1],dt[2])
        for i in rgb_clr.keys():
            if i[0] in range(tup[0]-15,tup[0]+15) and i[1] in range(tup[1]-15,tup[1]+15) and i[2] in range(tup[2]-15,tup[2]+15):
                self.war=rgb_clr[i][0]
        self.ids.lbl_clr.text=self.war
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
