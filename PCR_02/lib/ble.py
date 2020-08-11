from able import BluetoothDispatcher, GATT_SUCCESS,Advertisement
from kivy.properties import StringProperty,DictProperty,ListProperty
from jnius import autoclass
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
        if "ffe1" in uuid:
            value = characteristic.getStringValue(0)
            self.notification_value =str(value)
            self.dispatch("on_data_masuk")
    def on_state(self,a,b):
        self.do_toast(b)
    def do_toast(self,b):
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        PythonActivity.toastError(b)
    def on_data_masuk(self):
        pass