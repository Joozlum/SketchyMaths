import pickle
import shelve

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView

class SketchyLoad(Screen):
    root = None

    def __init__(self, **kwargs):
        super(SketchyLoad, self).__init__(**kwargs)
        self.sketchyloadbox = SketchyBox()
        self.sketchyloadbox.screen = self
        self.add_widget(self.sketchyloadbox)

    def on_enter(self, *args):
        super(SketchyLoad, self).on_enter(*args)
        self.sketchyloadbox.open_load()


class SketchyBox(BoxLayout):
    isopen = False
    sketchybook = []

    def __init__(self, **kwargs):
        super(SketchyBox, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.topbox = BoxLayout()
        self.topbox.orientation = 'vertical'
        self.topbox.size_hint_y = None
        self.topbox.bind(minimum_height=self.topbox.setter('height'))

        self.scrollview = ScrollView(size_hint=(1, 0.9), do_scroll_x=False, do_scroll_y=True)
        self.scrollview.add_widget(self.topbox)

        self.bottombox = BoxLayout()
        self.bottombox.orientation = 'horizontal'
        self.bottombox.size_hint_y = 0.1

        self.bottombox.b1 = Button()
        self.bottombox.b1.text = 'Close'
        self.bottombox.b1.bind(on_press=self.close_load)

        self.bottombox.add_widget(self.bottombox.b1)
        self.add_widget(self.scrollview)
        self.add_widget(self.bottombox)

    def close_load(self, target):
        if target.text is not 'Close':
            data = pickle.loads(self.sketchybook[target.text])
            self.parent.parent.load_data(data)
        if self.isopen:
            self.sketchybook.close()
            self.topbox.clear_widgets()
            self.isopen = False

        self.parent.parent.current = 'main'

    def open_load(self):
        if not self.isopen:
            self.sketchybook = shelve.open('data/SketchyBook')
            for save in self.sketchybook:
                new_button = Button(text=save, size_hint_y=None, height=40)
                self.topbox.add_widget(new_button)
                new_button.bind(on_press=self.close_load)
            self.isopen = True