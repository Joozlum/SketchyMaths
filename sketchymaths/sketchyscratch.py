import pickle
import shelve

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView


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

        self.scrollview = ScrollView(size_hint=(1, 0.8), do_scroll_x=False, do_scroll_y=True)
        self.scrollview.add_widget(self.topbox)

        self.bottombox = BoxLayout()
        self.bottombox.orientation = 'horizontal'
        self.bottombox.size_hint_y = 0.2

        self.bottombox.b1 = Button()
        self.bottombox.b1.text = 'Open'
        self.bottombox.b1.bind(on_press=self.open)

        self.bottombox.b2 = Button()
        self.bottombox.b2.text = 'Close'
        self.bottombox.b2.bind(on_press=self.close)

        self.bottombox.add_widget(self.bottombox.b1)
        self.bottombox.add_widget(self.bottombox.b2)
        self.add_widget(self.scrollview)
        self.add_widget(self.bottombox)

    def open(self, target):
        if not self.isopen:
            self.sketchybook = shelve.open('SketchyBook')
            for save in self.sketchybook:
                new_button = Button(text=save, size_hint_y=None, height=40)
                self.topbox.add_widget(new_button)
                new_button.bind(on_press=self.close)
            self.isopen = True

    def close(self, target):
        if target.text is not 'Close':
            print(pickle.loads(self.sketchybook[target.text]))
        if self.isopen:
            self.sketchybook.close()
            self.topbox.clear_widgets()
            self.isopen = False


class SketchyTestApp(App):

    def build(self):
        self.root = root = SketchyBox()
        return root

#  Run app
if __name__ == "__main__":
    SketchyTestApp().run()

