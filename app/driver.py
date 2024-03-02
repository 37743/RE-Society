# Driver Code
# ---
# import os
# os.environ["KIVY_NO_CONSOLELOG"] = "1"
import kivy
kivy.require('2.2.0')
# Kivy Packages
from kivy.config import Config
# Window Configuration
# Disable graphical annotation
Config.set('input', 'mouse', 'mouse,disable_multitouch')
# Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'borderless', 1)
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import (ScreenManager,
                                    FadeTransition)
# Screens
from screens import (splash,
                     home)
# YAML Reading
import yaml
from datetime import datetime

from screeninfo import get_monitors
for m in get_monitors():
    print(str(m))

class Run(App):
    ''' Driver code for the application, contains a screen manager
    that controls which interface is shown to the user at a time.'''
    def build(self):
        # Load YAML configuration file
        with open('app/scripts/settings/config.yaml', 'r') as yaml_file:
            self.config_data = yaml.safe_load(yaml_file)
        print(self.config_data)
        Window.size = (self.config_data['window_size_x'], self.config_data['window_size_y'])
        # Window.left = int((1366-self.config_data['window_size_x'])/2)
        self.screen_manager = ScreenManager(transition = FadeTransition())

        self.db_cred = {}
        self.user = ""
        self.icon = "app/assets/splash/logo_w.png"
        self.title = "RE:Society"
        self.splash = splash.Splash(name="Splash Screen")
        self.home = home.Home(name="Home Page")
        screens = [
                    # self.splash,
                    self.home,
                    ]
        for screen in screens:
            self.screen_manager.add_widget(screen)
        return self.screen_manager
    
    def open_settings(self, *largs):
        pass

if __name__ == '__main__':
    Window.maximize()
    # Window.fullscreen = 'auto'
    main = Run()
    main.run()