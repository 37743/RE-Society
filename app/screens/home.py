# Home Screen
# ---
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Rectangle
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.uix.textinput import TextInput
from functools import partial
import datetime
from dateutil.relativedelta import relativedelta
# MariaDB connector
import mysql.connector

ADAM = "app/assets/fonts/Antonio-VariableFont_wght.ttf"
ANTONIO = "app/assets/fonts/ADAM.CG PRO.otf"

def change_to_screen(*args, screen):
    ''' Changes the current screen in the Kivy application'''
    App.get_running_app().screen_manager.current = screen
    return

def make_img(encoded_data, path):
    ''' Writes the encoded image data to a file and returns the path'''
    filepath=path
    with open(filepath, 'wb') as f:
        f.write(encoded_data)
    return filepath

class View(Popup, FloatLayout):
    def __init__(self,
                 convict_list,
                 profession,
                 convict_idx,
                 **kwargs):
        super(View, self).__init__(**kwargs)
        self.box = BoxLayout(orientation="horizontal",
                             spacing=-10)
        self.img_float = FloatLayout(size_hint=(.5,.8),)
        self.img_float.add_widget(Image(source="app/assets/view/pic_frame.png",
                              size_hint=(None,None),
                              size=(275,300),
                              pos_hint={"center_x": .5, "center_y": .75}))
        self.img_float.add_widget(Image(source=f"app/assets/home/con_img{convict_idx}.png",
                              size_hint=(None,None),
                              size=(250,250),
                              pos_hint={"center_x": .5, "center_y": .75}))
        self.box.add_widget(self.img_float)
        self.info_float = FloatLayout()
        self.info_float.add_widget(Image(source="app/assets/view/data_BG.png",
                              size_hint=(None,None),
                              size=(512,400),
                              pos_hint={"center_x": .5, "center_y": .5}))
        self.info_float.add_widget(Label(text=convict_list[convict_idx][1] + " " + convict_list[convict_idx][2],
                                         font_name="Antonio",
                                         color='#0168aa',
                                         font_size=32,
                                         halign='left',
                                         pos_hint={'center_x': .485, 'center_y': .85},
                                         text_size=(400, None), size_hint=(None, None), width=300, height=50))
        self.info_float.add_widget(Label(text=profession,
                                         font_name="Adam",
                                         color='#707070',
                                         font_size=28,
                                         halign='left',
                                         pos_hint={'center_x': .4, 'center_y': .77},
                                         text_size=(300, None), size_hint=(None, None), width=300, height=50))
        self.info_float.add_widget(Label(text="Birth Date:                 "+convict_list[convict_idx][3].strftime("%Y-%m-%d")+
                                         "\nAdmission Date:         "+convict_list[convict_idx][4].strftime("%Y-%m-%d")+
                                         "\nRelease Date:            "+(convict_list[convict_idx][4]+relativedelta(months=convict_list[convict_idx][6])).strftime("%Y-%m-%d")+
                                         "\nCrime(s) Committed:  "+str(convict_list[convict_idx][5])+
                                         "\nSentence:                  "+str(convict_list[convict_idx][6])+" month(s)"
                                         "\nOverall Rating:           "+("Good" if convict_idx%2 else "Bad" if convict_idx%3 else "Average"\
                                                                                if convict_idx%5 else "Excellent" if convict_idx%7\
                                                                                      else "Poor" if convict_idx%11 else "Fair" if\
                                                                                          convict_idx%13 else "Very Good" if\
                                                                                            convict_idx%17 else "Very Bad" if convict_idx%19\
                                                                                                else "Very Poor" if convict_idx%23 else "Very Fair"),
                                         font_name="Adam",
                                         color='#1d242c',
                                         font_size=20,
                                         halign='left',
                                         pos_hint={'center_x': .4, 'center_y': .55},
                                         text_size=(300, None), size_hint=(None, None), width=300, height=50))
        self.info_float.add_widget(Label(text="Additional Information:",
                                         font_name="Adam",
                                         color='#707070',
                                         font_size=28,
                                         halign='center',
                                         pos_hint={'center_x': .5, 'center_y': .33}))
        self.btn_box = BoxLayout(orientation="horizontal",
                                 spacing=25,
                                 pos_hint={"center_x": .7, "center_y": .2})
        self.btn_box.add_widget(Button(text="",
                                        size=(167,46),
                                        size_hint=(None,None),
                                        background_normal="app/assets/view/print_btn.png",
                                        background_down="app/assets/view/print_btn.png",
                                        pos_hint={'center_x': .5, 'center_y': .5}))
        self.btn_box.add_widget(Button(text="",
                                        size=(167,46),
                                        size_hint=(None,None),
                                        background_normal="app/assets/view/edit_btn.png",
                                        background_down="app/assets/view/edit_btn.png",
                                        pos_hint={'center_x': .5, 'center_y': .5}))
        self.info_float.add_widget(self.btn_box)
        self.box.add_widget(self.info_float)
        self.title = ""
        self.separator_height = 0
        self.background = "app/assets/home/BG_w.png"
        self.size_hint=(.65,.7)
        self.add_widget(self.box)

class Convict(FloatLayout):
    ''' Represents the Convict Card'''
    def __init__(self,
                 name, 
                 profession,
                 func,
                 con,
                 img="app/assets/home/user_img.png",
                 **kwargs):
        ''' Sets up the UI elements for the Convict Card
        Args:
            img: str
                The path to the image of the convict
            name: str
                The name of the convict
            func: function
                The function to be called when the view button is clicked
            con: int
                The index of the convict
            profession: str
                The profession of the convict'''
        super(Convict, self).__init__(**kwargs)
        self.add_widget(Image(source="app/assets/home/user_card.png",
                             pos_hint={"center_x": .5, "center_y": .5}))
        self.add_widget(Image(source=img,
                              size_hint=(None,None),
                              size=(76,76),
                              pos_hint={"center_x": .5, "center_y": .7}))
        self.add_widget(Label(text=name,
                             font_name="Adam",
                             color='#707070',
                             font_size=18,
                             halign='center',
                             pos_hint={'center_x': .5, 'center_y': .4}))
        self.add_widget(Label(text=profession,
                             font_name="Adam",
                             color='#707070',
                             font_size=16,
                             halign='center',
                             pos_hint={'center_x': .5, 'center_y': .3}))
        view_btn = Button(text="",
                            size=(87,24),
                            size_hint=(None,None),
                            background_normal="app/assets/home/view_btn.png",
                            background_down="app/assets/home/view_btn.png",
                            pos_hint={'center_x': .5, 'center_y': .15})
        view_btn.bind(on_release=partial(func,
                                         profession=profession,
                                         convict_idx=con))
        self.add_widget(view_btn)

class Home(Screen, FloatLayout):
    ''' Represents the Splash Screen'''
    def _update_bg(self, instance, value):
        ''' Updates the background size and position
          based on the screen size'''
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def _view_convict(self, instance, profession, convict_idx):
        ''' Opens the convict view popup'''
        popup = View(convict_list=self.convicts,
                     profession=profession,
                     convict_idx=convict_idx)
        popup.open()
        
    def _generate_convicts(self):
        ''' Fetches the convict data from the database'''
        result = []
        try:
            db_cred = App.get_running_app().db_cred
            cn = mysql.connector.connect(
                            user=db_cred['user'],
                            password=db_cred['password'],
                            host=db_cred['host'],
                            database=db_cred['database'])
            print("Connected!")
            cr = cn.cursor()
            cr.callproc("get_con")
            for res in cr.stored_results():
                fetch = res.fetchall()
                for row in fetch:
                    result.append(row)
            cn.close()
        except mysql.connector.Error as e:
            print(f"{e}")
        return result

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
        #region Taskbar
        self.logo_blue = Image(source="app/assets/home/logo_b.png",
                                 size_hint=(None,None),
                                 pos_hint={"center_x": .1, "center_y": .9})
        self.add_widget(self.logo_blue)
        self.search_bar = Image(source="app/assets/home/search_bar.png",
                                 size_hint=(None,None),
                                 size=(475, 54),
                                 pos_hint={"center_x": .5, "center_y": .9})
        self.add_widget(self.search_bar)
        self.search_box = TextInput(hint_text="Search (e.g. Carpentry, Plumbing, etc.)",
                                   font_size=20,
                                   size_hint=(None,None),
                                   padding=(10,7.5),
                                   cursor_color='black',
                                   multiline=False,
                                   background_normal="",
                                   background_active="",
                                   size=(375, 40),
                                   pos_hint={"center_x": .52, "center_y": .9})
        self.add_widget(self.search_box)
        self.user_icon = Image(source="app/assets/home/user_icon.png",
                                 size_hint=(None,None),
                                 pos_hint={"center_x": .85, "center_y": .9})
        self.user_label = Label(text="Yousef Gomaa",
                                font_name="Adam",
                                color='#707070',
                                font_size=18,
                                halign='center',
                                pos_hint={'center_x': .9, 'center_y': .9})
        self.add_widget(self.user_icon)
        self.add_widget(self.user_label)
        #endregion
        #region Convict List
        self.convict_scroll = ScrollView(size=(App.get_running_app().window_size[0]-50,
                                               App.get_running_app().window_size[1]-225),
                                     size_hint=(None, None),
                                     pos_hint={"center_x": .5, "center_y": .4},
                                     bar_color = "#0168aa",
                                     bar_inactive_color = "#b3d7e7",
                                     bar_width = 12,
                                     scroll_type = ['bars','content'])
        self.convict_grid = GridLayout(cols=5,
                                    spacing=50,
                                    col_default_width=155,
                                    col_force_default=True,
                                    row_default_height=190,
                                    row_force_default=True,
                                    padding=(175,0),
                                    size_hint_y=None)
        self.convict_grid.bind(minimum_height=\
                                self.convict_grid.setter('height'))
        self.convict_scroll.add_widget(self.convict_grid)
        self.add_widget(self.convict_scroll)
        self.convicts = self._generate_convicts()
        for idx, convict in enumerate(self.convicts):
            self.convict_grid.add_widget(Convict(name=convict[1] + " " + convict[2],
                                                 profession="Carpenter" if not idx%7 else "Plumber" if not idx%5 else "Electrician" if not idx%3 else "Mason" if not idx%2 else "Painter",
                                                 con=idx,
                                                 func=self._view_convict,
                                                 img=make_img(convict[7], f"app/assets/home/con_img{idx}.png")))
        self.convict_grid.add_widget(Image(source="app/assets/home/add_card.png",
                                                pos_hint={"center_x": .5, "center_y": .5}))
        #endregion 
        # self.add_widget(self.footer)