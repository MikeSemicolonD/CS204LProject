import os
import kivy
import pickle
import numpy as np
import pandas as pd

from kivy.app import App
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stencilview import StencilView
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.properties import StringProperty
from kivy.uix.effectwidget import AdvancedEffectBase, EffectWidget, EffectBase, HorizontalBlurEffect

from numpy import array
from scipy import ndimage
from PIL import Image,ImageGrab
from sklearn.tree import DecisionTreeClassifier

# Prevents that red circle from popping up when hitting right mouse button
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

# Use this script's path to get to the model
script_path = os.path.abspath(__file__)
script_dir = os.path.split(script_path)[0]

# model_path = "C:\Users\Mike\Jupyter\CS204LProject\"+"DigitRecogModel"
model_path = os.path.join(script_dir, "DigitRecogModel")

loaded_model = pickle.load(open(model_path, 'rb'))

Window.clearcolor = (1, 1, 1, 1)

class MyPaintWidget(Widget):

    num = StringProperty()

    numLabel = Label(
        text='[ref=world][color=000000]Number[/color][/ref]',
        font_size='20sp',
        markup = True,
        pos=(700, 500))
    with numLabel.canvas:
        Color(0, 0, 0, .25)
        Rectangle(pos=numLabel.pos, size=numLabel.size)

    #widget.add_widget(numLabel)
    
    def on_touch_down(self, touch):                
        with self.canvas:
            Color(0, 0, 0) 
            touch.ud['line'] = Line(points=(touch.x, touch.y),width=40)

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]
        
    def getter(self,touch):
        self.export_to_png("screen.png")
        img = Image.open("screen.png")
        img.resize((784,784)).convert('LA').split()[-1].save("screen.png")
        img = Image.open("screen.png")
        
        img = img.resize((28,28),Image.NEAREST)
        arr = array(img)
        
        os.remove("screen.png")

        # Output what the models thinks it is
        print("Number: " + str(loaded_model.predict(arr.reshape(1,-1)))[1:-1])
        self.num = str(loaded_model.predict(arr.reshape(1,-1)))[1:-1]
        label = Label(
            text='[ref=world][color=000000]Number: ' + self.num + '[/color][/ref]',
            font_size='20sp',
            markup = True,
            pos=(700, 500))
        with label.canvas:
            Color(0, 0, 0, .25)
            Rectangle(pos=label.pos, size=label.size)

        self.add_widget(label)        
        
    def clear(self,touch):
        self.canvas.clear()

class MyPaintApp(App):
             
    def build(self):

        wid = MyPaintWidget(size_hint=(None, None), size=Window.size)
        
        screengrab_Btn = Button(text='Read Number',pos=(50,50),size=(50,50))
        screengrab_Btn.bind(on_press=wid.getter)
        
        clear_Btn = Button(text='Clear',pos=(50,50),size=(50,50))
        clear_Btn.bind(on_press=wid.clear)

        layout = BoxLayout(size_hint=(1, None), height=50)
        layout.add_widget(screengrab_Btn)

        layout.add_widget(clear_Btn)
       
        root=BoxLayout(orientation='vertical')
        root.add_widget(wid)
        root.add_widget(layout)
        #screengrab_Btn.disabled = True

        return root
        
if __name__ == '__main__':
    MyPaintApp().run()

