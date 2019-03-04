import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.stencilview import StencilView
from PIL import Image,ImageGrab
import numpy as np 
from numpy import array

import pickle

#example_dict = {1:"6",2:"2",3:"f"}

#pickle_out = open("dict.pickle","wb")
#pickle.dump(example_dict, pickle_out)
#pickle_out.close()

Window.clearcolor = (1, 1, 1, 1)

class MyPaintWidget(Widget):

    def on_touch_down(self, touch):                
        with self.canvas:
            
            Color(0, 0, 0) 
            touch.ud['line'] = Line(points=(touch.x, touch.y),width=20)

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]
    def getter(self,touch):
        self.export_to_png("screen.png")
        img = Image.open("screen.png")
        arr = array(img)
        #array = np.array(img)
        #print(array) # (100, 200) {% endhighlight %}
        print(arr)
    def clear(self,touch):
        self.canvas.clear()
        


class MyPaintApp(App):
             
    def build(self):
        wid = MyPaintWidget(size_hint=(None, None), size=Window.size)
        
        screengrab_Btn = Button(text='Screen Grab/Output Pixel Values',pos=(50,50),size=(50,50))
        screengrab_Btn.bind(on_press=wid.getter)
        
        clear_Btn = Button(text='Clear',pos=(50,50),size=(50,50))
        clear_Btn.bind(on_press=wid.clear)

        layout = BoxLayout(size_hint=(1, None), height=50)
        layout.add_widget(screengrab_Btn)

        layout.add_widget(clear_Btn)
       
        root=BoxLayout(orientation='vertical')
        root.add_widget(wid)
        root.add_widget(layout)

        return root

    
if __name__ == '__main__':
    MyPaintApp().run()

