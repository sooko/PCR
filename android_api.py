from kivy.logger import Logger
from jnius import JavaException, PythonJavaClass, autoclass, java_method
Camera = autoclass('android.hardware.Camera')
AndroidActivityInfo = autoclass('android.content.pm.ActivityInfo')
AndroidPythonActivity = autoclass('org.kivy.android.PythonActivity')
PORTRAIT = AndroidActivityInfo.SCREEN_ORIENTATION_PORTRAIT
LANDSCAPE = AndroidActivityInfo.SCREEN_ORIENTATION_LANDSCAPE
class ShutterCallback(PythonJavaClass):
    __javainterfaces__ = ('android.hardware.Camera$ShutterCallback', )
    @java_method('()V')
    def onShutter(self):
        pass
class PictureCallback(PythonJavaClass):
    __javainterfaces__ = ('android.hardware.Camera$PictureCallback', )
    def __init__(self, filename, on_success):
        super(PictureCallback, self).__init__()
        self.filename = filename
        self.on_success = on_success
    @java_method('([BLandroid/hardware/Camera;)V')
    def onPictureTaken(self, data, camera):
        s = data.tostring()
        # print(s)
        with open("/storage/emulated/0/DCIM/PCR/"+self.filename, 'wb') as f:
            f.write(s)
        camera.startPreview()
        self.on_success(self.filename)

class AutoFocusCallback(PythonJavaClass):
    __javainterfaces__ = ('android.hardware.Camera$AutoFocusCallback', )
    def __init__(self, filename, on_success):
        super(AutoFocusCallback, self).__init__()
        self.filename = filename
        self.on_success = on_success
    @java_method('(ZLandroid/hardware/Camera;)V')
    def onAutoFocus(self, success, camera):
        if success:
            Logger.info('xcamera: autofocus succeeded, taking picture...')
            shutter_cb = ShutterCallback()
            picture_cb = PictureCallback(self.filename, self.on_success)
            camera.takePicture(shutter_cb, None, picture_cb)
        else:
            Logger.info('xcamera: autofocus failed')
def take_picture(camera_widget, filename, on_success):
    camera = camera_widget._camera._android_camera
    params = camera.getParameters()
    params.setFocusMode("auto")
    camera.setParameters(params)
    cb = AutoFocusCallback(filename, on_success)
    Logger.info('xcamera: starting autofocus...')
    try:
        camera.autoFocus(cb)
    except JavaException as e:
        Logger.info('Error when calling autofocus: {}'.format(e))
def set_orientation(value):
    previous = get_orientation()
    AndroidPythonActivity.mActivity.setRequestedOrientation(value)
    return previous
def get_orientation():
    return AndroidPythonActivity.mActivity.getRequestedOrientation()
