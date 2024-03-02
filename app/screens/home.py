# Home Screen
# ---
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.clock import (mainthread,
                        Clock)
from kivy.animation import Animation
import time

ADAM = "app/assets/fonts/Antonio-VariableFont_wght.ttf"
ANTONIO = "app/assets/fonts/ADAM.CG PRO.otf"

def change_to_screen(*args, screen):
    ''' Changes the current screen in the Kivy application'''
    App.get_running_app().screen_manager.current = screen
    return

class Home(Screen, FloatLayout):
    ''' Represents the Splash Screen'''
    def _update_bg(self, instance, value):
        ''' Updates the background size and position
          based on the screen size'''
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def __init__(self, **kwargs):
        ''' Sets up UI elements and registering fonts'''
        super(Home, self).__init__(**kwargs)
        with self.canvas.before:
            self.bg = Rectangle(source="app/assets/home/BG_w.png",
                                size=self.size,
                                pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)
        LabelBase.register(name='Adam', fn_regular=ADAM)
        LabelBase.register(name='Antonio', fn_regular=ANTONIO)
        self.footer = Label(text="RE:Society is a comprehensive application aimed at reintegrating ex-convicts into society by providing them with job opportunities and mentorship.",
                             color = "ffffff",
                             text_size = (500, None),
                             font_name="Antonio",
                             halign="center",
                             pos_hint={"center_x": .5, "center_y": .04},
                             font_size=11)
        self.add_widget(self.footer)