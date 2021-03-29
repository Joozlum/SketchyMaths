from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView

from .textloader import load_text


class SketchyGuide(Screen):
    def __init__(self, **kwargs):
        super(SketchyGuide, self).__init__(**kwargs)
        self.box1 = BoxLayout()
        self.box1.orientation = 'vertical'
        self.scroll_view = ScrollView()
        self.scroll_view.do_scroll_x = False
        self.scroll_view.do_scroll_y = True
        self.scroll_view_label = Label()
        self.scroll_view_label.size_hint_y = None

        self.scroll_view_label.bind(width=self.width_bind_callback)
        self.scroll_view_label.bind(texture_size=self.height_bind_callback)

        self.scroll_view_label.padding = (10, 10)
        self.scroll_view_label.markup = True
        self.scroll_view_label.font_size = 20
        self.scroll_view_label.text = load_text('guide')

        self.box2 = BoxLayout()
        self.box2.orientation = 'horizontal'
        self.box2.size_hint_y = .1

        self.box2.b1 = Button()
        self.box2.b2 = Button()
        self.box2.b3 = Button()

        self.box2.b1.text = 'Guide'
        self.box2.b2.text = 'Shortcuts'
        self.box2.b3.text = 'Return'

        self.box2.b1.bind(on_press=self.button_callback)
        self.box2.b2.bind(on_press=self.button_callback)
        self.box2.b3.bind(on_press=self.button_callback)

        self.scroll_view.add_widget(self.scroll_view_label)
        self.box1.add_widget(self.scroll_view)

        self.box2.add_widget(self.box2.b1)
        self.box2.add_widget(self.box2.b2)
        self.box2.add_widget(self.box2.b3)

        self.bind(height=self.guide_height_callback)

        self.add_widget(self.box1)
        self.add_widget(self.box2)

    def guide_height_callback(self, target, value):
        self.box2.size_hint_y = 40 / value

    def button_callback(self, value):
        if value.text == 'Guide':
            self.scroll_view_label.text = load_text('guide')
        elif value.text == 'Shortcuts':
            self.scroll_view_label.text = load_text('methods')
        elif value.text == 'Return':
            self.screenmanager.current = 'main'

    def width_bind_callback(self, target, value):
        self.scroll_view_label.text_size = (value, None)

    def height_bind_callback(self, target, value):
        self.scroll_view_label.height = value[1] + 100
