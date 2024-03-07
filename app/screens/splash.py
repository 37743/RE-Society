# Splash Screen
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
from scripts.loading import CircularProgressBar
import threading
import time

ADAM = "app/assets/fonts/Antonio-VariableFont_wght.ttf"
ANTONIO = "app/assets/fonts/ADAM.CG PRO.otf"

def change_to_screen(*args, screen):
    ''' Changes the current screen in the Kivy application'''
    App.get_running_app().screen_manager.current = screen
    return

def thread(function):
    ''' Creates a new thread with a process using the input function'''
    def wrap(*args, **kwargs):
        t = threading.Thread(target=function, args=args, kwargs=kwargs, daemon=True)
        t.start()
        return t
    return wrap

class Splash(Screen, FloatLayout):
    ''' Represents the Splash Screen'''
    def _update_bg(self, instance, value):
        ''' Updates the background size and position
          based on the screen size'''
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def _load_program(self, instance):
        ''' Simulates a loading process with a placeholder time delay
        Triggers on button release, starting an animation and changing
        the screen after a delay'''
        if self.logobutton.disabled:
            return
        self.logobutton.disabled = True
        start_time = time.time()
        end_time = start_time + 4  # 4 seconds
        # TODO: Load actual material instead of placebo waiting time.
        self.add_widget(self.progress_bar)
        self._update_loading_pct(start_time, end_time)
    
    @mainthread
    def _update_pct(self, new_pct):
        self.loading_text.text = "Loading.. {p}%".format(p=new_pct)

    @thread
    def _update_loading_pct(self, start_time, end_time, *args):
        ''' Updates the loading text label with the current progress percentage'''
        self.loading_text.text = ""
        now = time.time()
        while now < end_time:
            prog_pct = min(100, round((time.time() - start_time) * 100 / (end_time - start_time)))
            # self._update_pct(prog_pct)
            self.progress_bar.set_value(prog_pct)
            if (prog_pct == 100):
                Clock.schedule_once(lambda dt: change_to_screen(screen="Login Page"), 1)
                break

    def _login_thread(self, instance):
        ''' Start loading up the program, including database connection'''
        login_thread = threading.Thread(target=self._load_program)
        login_thread.start()

    def __init__(self, **kwargs):
        ''' Sets up UI elements and registering fonts'''
        super(Splash, self).__init__(**kwargs)
        with self.canvas.before:
            self.bg = Rectangle(source="app/assets/splash/BG_blue.png",
                                size=self.size,
                                pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)
        LabelBase.register(name='Adam', fn_regular=ADAM)
        LabelBase.register(name='Antonio', fn_regular=ANTONIO)
        self.logobutton = Button(size_hint=(None,None),
                                 size=(178,153),
                                 pos_hint={"center_x": .5, "center_y": .55},
                                 background_normal="app/assets/splash/logo_w2.png",
                                 background_disabled_normal="app/assets/splash/logo_w2.png",
                                 background_down="app/assets/splash/logo_w.png")
        self.logobutton.bind(on_release=self._load_program,
                            #  on_press=click_sfx
                             )
        self.loading_text = Label(text="Connecting to server..",
                                  font_name="Antonio",
                                  color="ffffff",
                                  font_size=22,
                                  pos_hint={'center_x': .5, 'center_y': .4},
                                  halign='center')
        self.progress_bar = CircularProgressBar(max=100,
                                                height=125,
                                                width=125,
                                                size_hint = (None, None))
        self.add_widget(self.logobutton)
        self.add_widget(self.loading_text)
        self.footer = Label(text="RE:Society is a comprehensive application aimed at reintegrating ex-convicts into society by providing them with job opportunities and mentorship.",
                             color = "ffffff",
                             text_size = (500, None),
                             font_name="Antonio",
                             halign="center",
                             pos_hint={"center_x": .5, "center_y": .04},
                             font_size=11)
        self.add_widget(self.footer)
        self.schedule_connection = Clock.schedule_once(self._load_program, 3)