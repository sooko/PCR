import datetime
import os
from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.resources import resource_add_path
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty,ListProperty,BooleanProperty
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.clock import Clock
import PIL
from PIL import ImageOps
from PIL import Image as Gambar
if platform == 'android':
    from .android_api import (LANDSCAPE, PORTRAIT, take_picture, set_orientation, get_orientation)
from binascii import hexlify,unhexlify
from numpy import asarray

def get_filename():
    return datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S')
def is_android():
    return platform == 'android'
def check_camera_permission():
    if not is_android():
        return True
    from android.permissions import Permission, check_permission
    permission = Permission.CAMERA
    return check_permission(permission)
def check_request_camera_permission(callback=None):
    had_permission = check_camera_permission()
    if not had_permission:
        from android.permissions import Permission, request_permissions
        permissions = [Permission.CAMERA]
        request_permissions(permissions, callback)
    return had_permission
Builder.load_string("""
<XCameraIconButton>
    icon_color: (0, 0, 0, 1)
    _down_color: 1,1,1,1
    icon_size: dp(50)
    canvas.before:
        Color:
            rgba: self.icon_color if self.state == 'normal' else self._down_color
        Ellipse:
            pos: self.pos
            size: self.size
    size_hint: None, None
    size: self.icon_size, self.icon_size
    font_size: self.icon_size/2

<XCamera>:
    pos_hint:{"center_x":.5,"center_y":.5}
    icon: u"[font=data/icons.ttf]\ue800[/font]"
    icon_color: (0.13, 0.58, 0.95, 0.8)
    id: camera
    resolution: 1920, 1080
    allow_stretch: True
    icon: u"[font=data/icons.ttf]\ue800[/font]"
    icon_size: dp(70)
    # size_hint:.5,.5
    XCameraIconButton:
        id: shoot_button
        markup: True
        text: root.icon
        icon_color: root.icon_color
        icon_size: root.icon_size
        on_release: root.shoot("test")
        right: root.width - dp(5)
        center_y: root.center_y
<LCamera>:
    pos_hint:{"center_x":.5,"center_y":.5}
    resolution: 1920, 1080
    Button:
        background_color:0,0,0,0
        pos_hint:{"center_x":.5,"center_y":.5}
    Image
        pos_hint:{"center_x":.5,"center_y":.5}
        id:img
""")

class XCameraIconButton(ButtonBehavior, Label):
    pass
class XCamera(Camera):
    directory = ObjectProperty(None)
    _previous_orientation = None
    __events__ = ('on_picture_taken', 'on_camera_ready')
    arrtexture=ObjectProperty(None,allownone=True)
    warna=ListProperty([])
    played=BooleanProperty(False)
    def __init__(self, **kwargs):
        # Builder.load_file("cam/xcamera.kv")
        self.register_event_type("on_back")
        super().__init__(**kwargs)
    def _on_index(self, *largs):
        @mainthread
        def on_permissions_callback(permissions, grant_results):
            if all(grant_results):
                self._on_index_dispatch(*largs)
        if check_request_camera_permission(callback=on_permissions_callback):
            self._on_index_dispatch(*largs)
    def _on_index_dispatch(self, *largs):
        super()._on_index(*largs)
        self.dispatch('on_camera_ready')
    def on_picture_taken(self, filename):
        pass
    def on_camera_ready(self):
        pass
    def on_tex(self, *l):
        image_data = self.arrtexture.pixels
        size = self.arrtexture.size
        pil_image = PIL.Image.frombytes(mode='RGBA', size=size, data=image_data)
        data=asarray(pil_image)
        b = (data[int(size[1]/2), int(size[0]/2)])
        self.warna=b.tolist()
        if self.played:
            self.canvas.ask_update()
            self.texture=self.arrtexture
            self.texture_size=self.arrtexture_size
    def _camera_loaded(self, *largs):
        self.arrtexture = self._camera.texture
        self.arrtexture_size = list(self.arrtexture.size)
    def shoot(self,tittle):
        def on_success(filename):
            self.dispatch('on_picture_taken', filename)
        filename = get_filename()
        take_picture(self, filename+" nama="+tittle+".jpg", on_success)
    def on_back(self):
        self.played=False

from kivy.uix.image import Image
from kivy.graphics.texture import Texture
import cv2
import numpy as np
from kivy.uix.floatlayout import FloatLayout
class LCamera(FloatLayout):
    play=BooleanProperty(True)
    def __init__(self,*args, **kwargs):
        self.register_event_type("on_back")
        super(LCamera, self).__init__(*args,**kwargs)
        self.capture = cv2.VideoCapture(1)
        Clock.schedule_interval(self.update, .05)
    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            buf1 = cv2.flip(frame, 0)#cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_blue = np.array([110,50,50])
            upper_blue = np.array([130,255,255])
            mask = cv2.inRange(buf1, lower_blue, upper_blue)
            res = cv2.bitwise_and(frame,frame, mask= mask)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.ids.img.texture = image_texture
    def on_back(self):
        self.play=False
    def on_play(self,instance,value):
        if value:
            self.capture=cv2.VideoCapture(1)
            Clock.schedule_interval(self.update, .1)
        else:
            self.capture.release()
            Clock.unschedule(self.update)

