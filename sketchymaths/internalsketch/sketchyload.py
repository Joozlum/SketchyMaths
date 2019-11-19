import pickle
import shelve

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

        self.bottombox.load_examples_button = Button()
        self.bottombox.load_examples_button.text = 'Load Examples'
        self.bottombox.load_examples_button.bind(on_press=self.examples_load)
        self.bottombox.load_examples_button.size_hint_x = .20

        self.bottombox.load_autosaves_button = Button()
        self.bottombox.load_autosaves_button.text = 'Load Auto-Saves'
        self.bottombox.load_autosaves_button.bind(on_press=self.auto_saves_load)
        self.bottombox.load_autosaves_button.size_hint_x = .20

        self.bottombox.b1 = Button()
        self.bottombox.b1.text = 'Close'
        self.bottombox.b1.bind(on_press=self.close_load)
        self.bottombox.b1.size_hint_x = .60

        self.bottombox.add_widget(self.bottombox.load_examples_button)
        self.bottombox.add_widget(self.bottombox.load_autosaves_button)
        self.bottombox.add_widget(self.bottombox.b1)
        self.add_widget(self.scrollview)
        self.add_widget(self.bottombox)

        self.bind(height=self.height_callback)

    def height_callback(self, target, value):
        self.bottombox.size_hint_y = 60 / value

    def close_load(self, target):
        if target.text is not 'Close':
            data = pickle.loads(self.sketchybook[target.text])
            self.parent.parent.load_data(data)
        if self.isopen:
            self.sketchybook.close()
            self.topbox.clear_widgets()
            self.isopen = False

        self.parent.parent.current = 'main'

    def open_load(self, load_type='normal'):
        if not self.isopen:
            if load_type == 'examples':
                self.sketchybook = shelve.open('data/SketchyExamples')
            elif load_type == 'autosaves':
                self.sketchybook = shelve.open('data/AutoSaves')
            else:
                self.sketchybook = shelve.open('data/SketchyBook')
            i = 0
            for save in self.sketchybook:
                save_line = BoxLayout(size_hint_y=None, height=40)
                load_button = Button(text=save, size_hint_x=.9)
                delete_button = Button(text='Delete', size_hint_x=.1)
                save_line.add_widget(load_button)
                save_line.add_widget(delete_button)
                self.topbox.add_widget(save_line, i)
                delete_button.save = save
                delete_button.save_line = save_line
                load_button.bind(on_press=self.close_load)
                delete_button.bind(on_release=self.delete_save)
                i += 1
            self.isopen = True

    def examples_load(self, target):
        if self.isopen:
            self.sketchybook.close()
            self.isopen = False
            self.topbox.clear_widgets()
            self.open_load('examples')

    def auto_saves_load(self, target):
        if self.isopen:
            self.sketchybook.close()
            self.isopen = False
            self.topbox.clear_widgets()
            self.open_load('autosaves')

    def delete_save(self, target):
        del self.sketchybook[target.save]
        self.topbox.remove_widget(target.save_line)

