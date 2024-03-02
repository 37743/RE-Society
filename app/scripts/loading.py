# Circular Loading Bar
# ---
from kivy import utils
from kivy.uix.progressbar import ProgressBar
from kivy.core.text import Label as CoreLabel
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.clock import (mainthread,
                        Clock)
from kivy.animation import Animation
import threading

# def hide(*args, self, instance):
#     hide = Animation(opacity=0, t='in_cubic', d=1)
#     hide.start(instance)

# def show(*args, self, instance):
#     show = Animation(opacity=1, t='in_cubic', d=1)
#     show.start(instance)

def thread(function):
    ''' Creates a new thread with a process using the input function'''
    def wrap(*args, **kwargs):
        t = threading.Thread(target=function, args=args, kwargs=kwargs, daemon=True)
        t.start()
        return t
    return wrap

class CircularProgressBar(ProgressBar):
    def __init__(self, **kwargs):
        super(CircularProgressBar, self).__init__(**kwargs)
        self.thickness = 22
        self.pos = (-200, 0)
        # show(self=self, instance=self)
        self.pos_hint = {'center_x': .5, 'center_y': .3}
        self.label = CoreLabel(text="0%",
                               font_size=self.thickness,
                               font_family="Antonio")
        self.texture_size = None
        self.canvas.clear()
        self.refresh_text()
        self.draw()
            
    @mainthread
    def draw(self):
        # gray = utils.get_color_from_hex('#707070')[:3]
        white = utils.get_color_from_hex('#fafafa')[:3]
        blue = utils.get_color_from_hex('#0069aa')[:3]
        with self.canvas:
            self.canvas.clear()
            
            Color(blue[0], blue[1], blue[2])
            Ellipse(pos=self.pos, size=self.size)

            # Draw progress circle, small hack if there is no progress (angle_end = 0 results in full progress)
            Color(white[0], white[1], white[2])
            Ellipse(pos=self.pos, size=self.size,
                    angle_end=(0.001 if self.value_normalized == 0 else self.value_normalized*360))

            # Draw the inner circle (colour should be equal to the background)
            Color(blue[0], blue[1], blue[2])
            Ellipse(pos=(self.pos[0] + self.thickness / 2, self.pos[1] + self.thickness / 2),
                    size=(self.size[0] - self.thickness, self.size[1] - self.thickness))

            # Center and draw the progress text
            Color(white[0], white[1], white[2])
            #added pos[0]and pos[1] for centralizing label text whenever pos_hint is set
            Rectangle(texture=self.label.texture, size=self.texture_size,
                  pos=(self.size[0] / 2 - self.texture_size[0] / 2 + self.pos[0], self.size[1] / 2 - self.texture_size[1] / 2 + self.pos[1]))

    @mainthread
    def refresh_text(self):
        self.label.refresh()
        self.texture_size = list(self.label.texture.size)

    @thread
    def set_value(self, value):
        self.value = value
        self.label.text = str(value)+"%"
        self.refresh_text()
        self.draw()