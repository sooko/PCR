import datetime
import os
from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.resources import resource_add_path
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty,ListProperty
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
    return datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S.jpg')
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
class XCameraIconButton(ButtonBehavior, Label):
    pass
class XCamera(Camera):
    directory = ObjectProperty(None)
    _previous_orientation = None
    __events__ = ('on_picture_taken', 'on_camera_ready')
    arrtexture=ObjectProperty(None,allownone=True)
    warna=ListProperty([])
    def __init__(self, **kwargs):
        Builder.load_file("cam/xcamera.kv")
        self.register_event_type("on_back")
        super().__init__(**kwargs)
        # self.play=False
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
        print(self.warna)
        if self.play:
            self.canvas.ask_update()
            self.texture=self.arrtexture
            self.texture_size=self.arrtexture_size

    def _camera_loaded(self, *largs):
        self.arrtexture = self._camera.texture
        self.arrtexture_size = list(self.arrtexture.size)
    def shoot(self):
        def on_success(filename):
            self.dispatch('on_picture_taken', filename)
        filename = get_filename()
        take_picture(self, filename, on_success)
    def on_back(self):
        pass




from kivy.uix.image import Image
from kivy.graphics.texture import Texture
import cv2
import numpy as np
from kivy.uix.floatlayout import FloatLayout

class LCamera(FloatLayout):
    Builder.load_file("cam/xcamera.kv")
    def __init__(self,*args, **kwargs):
        self.register_event_type("on_back")
        super(LCamera, self).__init__(*args,**kwargs)
        self.capture = cv2.VideoCapture(1)
        Clock.schedule_interval(self.update, .1)
    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            buf1 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)#cv2.flip(frame, 0)
            lower_blue = np.array([110,50,50])
            upper_blue = np.array([130,255,255])
            mask = cv2.inRange(buf1, lower_blue, upper_blue)
            res = cv2.bitwise_and(frame,frame, mask= mask)
            buf = res.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.ids.img.texture = image_texture
            # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # lower_blue = np.array([110,50,50])
            # upper_blue = np.array([130,255,255])
            # mask = cv2.inRange(hsv, lower_blue, upper_blue)
            # res = cv2.bitwise_and(frame,frame, mask= mask)
            
    def on_back(self):
        pass
            
# class CamApp(App):
#     def build(self):
#         self.capture = cv2.VideoCapture(1)
#         self.my_camera = KivyCamera(capture=self.capture, fps=30)
#         return self.my_camera
#     def on_stop(self):
#         self.capture.release()

# if __name__ == '__main__':
#     CamApp().run()
