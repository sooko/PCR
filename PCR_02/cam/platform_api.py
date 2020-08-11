from kivy.utils import platform
if platform == 'android':
    from .android_api import (LANDSCAPE, PORTRAIT, take_picture, set_orientation, get_orientation)
else:
    pass
