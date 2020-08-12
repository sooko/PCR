from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
Builder.load_string("""
<Kotak>:
    canvas:
        Color:
            rgba:0,0,0,.1
        Line:
            rectangle:(self.x,self.y,self.width,self.height)
<Xlabel>:
    color:0,0,0,1
    font_size:dp(10)
<Ylabel>:
    color:0,0,0,1
    font_size:dp(10)

<Chart>:
    FloatLayout
        pos_hint:{"center_x":.5,"center_y":.5}
        size_hint:None,None
        size:root.width-dp(5),root.height-dp(5)
        canvas:
            Color:
                rgba:0,0,0,.2
            Rectangle:
                size:self.size
                pos:self.pos
            Color:
                rgba:1,1,1,.6
            Rectangle:
                size:self.size
                pos:self.pos
        BoxLayout
            size_hint:None,None
            size:self.parent.size[0]-dp(10),self.parent.size[1]-dp(10)
            BoxLayout:
                orientation:"vertical"
                size_hint:None,1
                width:dp(25)
                BoxLayout:
                    orientation:"vertical"
                    id:root_y_label
                    canvas.before:
                        PushMatrix:
                        Translate:
                            y:(self.height/root.major_y/2)
                    canvas.after:
                        PopMatrix:
                Label
                    text:"0"
                    font_size:dp(10)
                    color:0,0,0,1
                    size_hint:1,None
                    height:dp(25)
            BoxLayout:
                orientation:"vertical"
                size_hint:1,1
                FloatLayout
                    canvas:
                        Color:
                            rgba:0,0,0,1
                        Rectangle:
                            size:dp(1.5),self.size[1]
                            pos:self.pos
                        Color:
                            rgba:0,0,0,1
                        Rectangle:
                            size:self.size[0],dp(1.5)
                            pos:self.pos
                    GridLayout
                        pos_hint:{"center_x":.5,"center_y":.5}
                        cols:root.major_x
                        id:root_kotak   
                BoxLayout:
                    id:root_x_label
                    size_hint:1,None
                    height:dp(25)
                    canvas.before:
                        PushMatrix:
                        Translate:
                            x:(self.width/root.major_x/2)
                    canvas.after:
                        PopMatrix:

 """)
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
class Kotak(Widget):
    pass
class Xlabel(Label):
    pass
class Ylabel(Label):
    pass
from kivy.uix.button import Button
from kivy.properties import StringProperty,NumericProperty
class Chart(FloatLayout):
    major_x=NumericProperty(1)
    major_y=NumericProperty(1)
    def __init__(self,*args,**kwargs):
        super(Chart,self).__init__(*args,**kwargs)

    def on_major_x(self,a,b):
        Clock.schedule_once(self.delay,5)
    def delay(self,dt):
        self.ids.root_kotak.clear_widgets()
        self.ids.root_x_label.clear_widgets()
        self.ids.root_y_label.clear_widgets()
        for i in range(self.major_x * self.major_y):
            self.ids.root_kotak.add_widget(Kotak())
        if self.major_x<=50:
            for i in range(self.major_x):
                self.ids.root_x_label.add_widget(Xlabel(text=str(i+1)))
        else:
            for i in range(self.major_x):
                self.ids.root_x_label.add_widget(Xlabel(text="I"))
        for i in range(self.major_y):
            self.ids.root_y_label.add_widget(Ylabel(text=str(self.major_y-i)))
        


