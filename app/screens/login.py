# Login Screen
# ---
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.clock import (mainthread,
                        Clock)
# MariaDB Connector
import mysql.connector
from screens import home

ADAM = "app/assets/fonts/Antonio-VariableFont_wght.ttf"
ANTONIO = "app/assets/fonts/ADAM.CG PRO.otf"

def change_to_screen(*args, screen):
    ''' Changes the current screen in the Kivy application'''
    App.get_running_app().screen_manager.current = screen
    return

class Login(Screen, FloatLayout):
    ''' Represents the Splash Screen'''
    def _update_bg(self, instance, value):
        ''' Updates the background size and position
          based on the screen size'''
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def _login_released(self, instance):
        ''' Connects to database and verifies the input credentials'''
        try:
            app = App.get_running_app()
            db_cred = app.db_cred
            cn = mysql.connector.connect(
                            user=db_cred['user'],
                            password=db_cred['password'],
                            host=db_cred['host'],
                            database=db_cred['database'])
            cr = cn.cursor()
            u, p= str(self.user_box.text), str(self.pass_box.text)
            cr.execute(f"SELECT verify_login(\'{u}\',\'{p}\') AS verify_login")
            if cr.fetchall()[0][0] == 1:
                app.user = u
                app.home = home.Home(name="Home Page")
                app.screen_manager.add_widget(app.home)
                Clock.schedule_once(lambda dt: change_to_screen(screen="Home Page"), 2)
                self.login_results.text = "Success! Logging in.."
                self.login_results.color = "green"
            else:
                self.login_results.color = "red"
                self.login_results.text = "Invalid Credentials!"
            cn.close()
        except mysql.connector.Error as e:
            self.login_results.color = "red"
            self.login_results.text = "Server is offline."
            print(f"{e}")

    def __init__(self, **kwargs):
        ''' Sets up UI elements and registering fonts'''
        super(Login, self).__init__(**kwargs)
        with self.canvas.before:
            self.bg = Rectangle(source="app/assets/home/BG_w.png",
                                size=self.size,
                                pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)
        LabelBase.register(name='Adam', fn_regular=ADAM)
        LabelBase.register(name='Antonio', fn_regular=ANTONIO)
        #region Login Details
        self.logo_black = Image(source="app/assets/login/logo_b.png",
                                 size_hint=(None,None),
                                 pos_hint={"center_x": .5, "center_y": .8})
        self.add_widget(self.logo_black)
        self.login_layout = BoxLayout(orientation="vertical",
                                size_hint=(None,None),
                                size=(295,275),
                                padding=(20,15),
                                spacing=-20,
                                pos_hint={'center_x': .5, 'center_y': .52},)
        self.profile_pic = Image(source="app/assets/login/user_img.png",
                                 size=(75,75),
                                 size_hint=(None,None),
                                 pos_hint={"center_x": .5, "center_y": .5})
        self.login_layout.add_widget(self.profile_pic)
        self.user_label = Label(text="Phone Number",
                                font_name="Antonio",
                                color="0069aa",
                                font_size=13,
                                halign='left',
                                pos_hint={'center_x': .33, 'center_y': .5})
        self.login_layout.add_widget(self.user_label)
        self.user_box = TextInput(text="",
                                  multiline=False,
                                  size_hint = (.75,.4),
                                  font_name="Antonio",
                                  input_filter='int',
                                  cursor_color="1d242c",
                                  font_size=13,
                                  foreground_color="1d242c",
                                  write_tab=False,
                                  padding=(10,10),
                                  hint_text = "",
                                  background_normal="app/assets/login/textBox.png",
                                  background_active="app/assets/login/textBox.png",
                                  pos_hint={'center_x': .5, 'center_y': .5})
        self.login_layout.add_widget(self.user_box)
        self.pass_label = Label(text="Password",
                                font_name="Antonio",
                                color="0069aa",
                                font_size=13,
                                halign='left',
                                pos_hint={'center_x': .27, 'center_y': .5})
        self.login_layout.add_widget(self.pass_label)
        self.pass_box = TextInput(text="",
                                multiline=False,
                                size_hint = (.75,.4),
                                font_name="Antonio",
                                password=True,
                                cursor_color="1d242c",
                                font_size=13,
                                foreground_color="1d242c",
                                write_tab=False,
                                padding=(10,10),
                                hint_text = "",
                                background_normal="app/assets/login/textBox.png",
                                background_active="app/assets/login/textBox.png",
                                pos_hint={'center_x': .5, 'center_y': .5})
        self.login_layout.add_widget(self.pass_box)
        self.login_panel = Image(source="app/assets/login/login_card.png",
                                size_hint=(None,None),
                                size=(295,380),
                                pos_hint={"center_x": .5, "center_y": .46})
        self.add_widget(self.login_panel)
        self.add_widget(self.login_layout)
        self.login_button = Button(text="",
                                size_hint=(None,None),
                                size=(167,46),
                                pos_hint={'center_x': .5, 'center_y': .3},
                                background_normal=
                                "app/assets/login/login_btn.png",
                                background_down=
                                "app/assets/login/login_btn_down.png")
        self.login_button.bind(on_release=self._login_released)
        self.add_widget(self.login_button)
        self.login_results = Label(text="",
                                font_name="Antonio",
                                color='red',
                                font_size=13,
                                halign='center',
                                pos_hint={'center_x': .5, 'center_y': .24})
        self.add_widget(self.login_results)
        #endregion
        self.footer = Label(text="RE:Society is a comprehensive application aimed at reintegrating ex-convicts into society by providing them with job opportunities and mentorship.",
                             color = "707070",
                             text_size = (500, None),
                             font_name="Antonio",
                             halign="center",
                             pos_hint={"center_x": .5, "center_y": .04},
                             font_size=11)
        self.add_widget(self.footer)