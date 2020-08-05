import datetime
import os
from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.resources import resource_add_path
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.clock import Clock

from platform_api import LANDSCAPE, set_orientation, take_picture
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
    array_cam=ObjectProperty(None)
    def __init__(self, **kwargs):
        Builder.load_file("xcamera.kv")
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
    # def on_texture(self,a,b):
    #     print(self.texture.pixels)
    def shoot(self):
        def on_success(filename):
            self.dispatch('on_picture_taken', filename)
        filename = get_filename()
        take_picture(self, filename, on_success)
        # m=self.texture.pixels
        # f=open("/storage/emulated/0/DCIM/PCR/l.jpg","wb")
        # f.write(m)
        # f.close()
        
        