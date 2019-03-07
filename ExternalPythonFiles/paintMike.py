from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.stencilview import StencilView
from functools import partial
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
import pickle
import pandas as pd
from sklearn.tree import DecisionTreeClassifier


# Works relative to my path, Python has a library that can setup our directory for us.
loaded_model = pickle.load(open("C:/Users/Mike/Jupyter/PickleObjects/DigitRecogModel", 'rb'))

Window.clearcolor = (1, 1, 1, 1)
Window.size = (800,600)

class MyPaintWidget(StencilView):
             
    def on_touch_down(self, touch):                
        with self.canvas:
            
            #Color(255, 255, 255)
            #Rectangle(pos=(10, 10), size=(500, 500))
            
            Color(0, 0, 0) 
            touch.ud['line'] = Line(points=(touch.x, touch.y),width=20)
         
    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]
        



class MyPaintApp(App):

    def resetCanvas(self,widget, *largs):
        widget.canvas.clear()

    def build(self):

        StencilPaintWid = MyPaintWidget(size_hint=(None,None), size = (400,300))
        
        canvasLayout = BoxLayout(size_hint=(1,None),height=50)
        
        clearButton = Button(text='Clear')
        clearButton.bind(on_press=partial(self.resetCanvas,'Clear',StencilPaintWid))

        canvasLayout.add_widget(clearButton)

        floatingLayout = FloatLayout(pos=(Window.height/2,Window.width/2))

        floatingLayout.add_widget(StencilPaintWid)

        root = BoxLayout(orientation='vertical')
        root.add_widget(floatingLayout)
        root.add_widget(canvasLayout)
            
        return root
    

if __name__ == '__main__':
    MyPaintApp().run()

