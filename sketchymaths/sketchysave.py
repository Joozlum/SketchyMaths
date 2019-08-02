import datetime
import pickle
import shelve

from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


class labelsavename(Label):
    pass


class SketchySave(Screen):

    def on_enter(self, *args):
        super(SketchySave, self).on_enter(*args)
        self.savenametextinput.text = str(datetime.datetime.today())
        self.callback_size_y(height=self.height)
        self.callback_size_x(width=self.width)
        self.previous_saves()


    def previous_saves(self):
        self.paddingbox.text = 'Previous Saves:\n'
        sketchybook = shelve.open('data/SketchyBook')
        for save in sketchybook:
            self.paddingbox.text += '\n'
            self.paddingbox.text += "{save}".format(save=save)
        sketchybook.close()

    def __init__(self, **kwargs):
        super(SketchySave, self).__init__(**kwargs)
        self.saveboxlayout = BoxLayout()
        self.saveboxlayout.orientation = 'vertical'

        self.savetextbox = BoxLayout()
        self.savetextbox.orientation = 'horizontal'

        self.labelsavename = labelsavename()
        self.labelsavename.text = 'Name this save file:'
        self.labelsavename.font_size = 25

        self.labelsavestatus = Label()
        self.labelsavestatus.font_size = 25
        self.labelsavestatus.text = ''
        self.labelsavestatus.color = (0, 1, 0, 1)

        self.savenametextinput = TextInput()
        self.savenametextinput.text = str(datetime.datetime.today())

        self.paddingbox = Label()
        self.paddingbox.valign = 'top'
        self.paddingbox.padding = (20, 20)
        self.paddingbox.font_size = 20

        self.buttonbox = BoxLayout()

        self.savebutton = Button()
        self.savebutton.text = 'Save'
        self.savebutton.bind(on_release=self.callback_savebutton)

        self.returnbutton = Button()
        self.returnbutton.text = 'Return'
        self.returnbutton.bind(on_release=self.callback_returnbutton)

        self.buttonbox.add_widget(self.savebutton)
        self.buttonbox.add_widget(self.returnbutton)

        self.savetextbox.add_widget(self.labelsavename)
        self.savetextbox.add_widget(self.labelsavestatus)

        self.saveboxlayout.add_widget(self.savetextbox)
        self.saveboxlayout.add_widget(self.savenametextinput)
        self.saveboxlayout.add_widget(self.paddingbox)
        self.saveboxlayout.add_widget(self.buttonbox)

        self.add_widget(self.saveboxlayout)
        self.bind(height=self.callback_size_y)
        self.bind(width=self.callback_size_x)

    def callback_size_y(self, target=None, height=100):
        self.savetextbox.size_hint_y = 120 / height
        self.savenametextinput.size_hint_y = 40 / height
        self.paddingbox.size_hint_y = (height - 220) / height
        self.buttonbox.size_hint_y = 60 / height
        self.paddingbox.text_size = self.paddingbox.size

    def callback_size_x(self, target=None, width=100):
        self.paddingbox.text_size = self.paddingbox.size


    def get_equation_dictionary(self):
        equation_dictionary = self.parent.save_data()
        data = []
        for inst in equation_dictionary.values():
            x = (inst.equation_id, inst.pos, inst.equation_text, inst.equationlabel.font_size)
            data.append(x)
        return data

    def save_to_book(self, data):
        """

        :type data: list
        """
        sketchybook = shelve.open('data/SketchyBook')
        sketchybook[self.savenametextinput.text] = pickle.dumps(data)
        sketchybook.close()

    def callback_savebutton(self, target):
        self.save_to_book(self.get_equation_dictionary())

        self.labelsavestatus.text = self.savenametextinput.text + '\nSaved!'
        self.labelsavestatus.text += '\n' + str(datetime.datetime.now())
        self.previous_saves()

    def callback_returnbutton(self, target):
        #  Return to 'main' window
        self.parent.current = 'main'
