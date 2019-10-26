from kivy import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.uix.textinput import TextInput
from sketchymaths.internalsketch.equations import Equation
from sketchymaths.internalsketch.sketchystatic import process_connections


class GenericLabel(Label):
    pass

class EquationTextInput(TextInput):
    pass

class EquationLabel(Label):
    pass

class EquationEditor:
    """
        This class controls the text inputs, and takes in binding calls.
        It also controls any functions that happen inside of the text inputs.

        The goal here is to separate out these controls and simplify the code
        that happens inside of the app itself.

        The interface with it will be extremely simple as well.

        It only needs to take in two commands.

        Switch Focus:
            This would take in an equation and refresh and rebind the text

        Clear Focus:
            This would clear any bindings, clear the text, and make it not accept text
            input until a new focus is sent.

        It will also play a minor role in garbage collection, as it would send a
        delete signal to BlackBoard if the equation losing focus is empty.
    """

    current_equation: Equation
    equation_name_editor: TextInput
    equation_text_editor: TextInput

    def __init__(self, equation_name_editor, equation_text_editor, **kwargs):
        #  References to the two text inputs it'll control
        self.equation_name_editor = equation_name_editor
        self.equation_text_editor = equation_text_editor

        #  Property to hold the equation it is editing
        self.current_equation = None

        #  Bind text in each to a callback
        self.equation_name_editor.bind(text=self.name_text_callback)
        self.equation_text_editor.bind(text=self.equation_text_callback)

    def change_focus(self, equation: Equation):
        to_delete = None
        if self.current_equation:
            if self.current_equation.equation_text == '':
                to_delete = self.current_equation

        #  Only run if equation is different
        if self.current_equation is not equation:
            self.current_equation = equation
            self.equation_name_editor.text = equation.equation_id
            self.equation_text_editor.text = equation.equation_text

        self.equation_text_editor.focus = True
        Clock.schedule_once(lambda x: self.equation_text_editor.select_all())
        return to_delete

    def clear_focus(self):
        #  Clear bindings from current equation if not None

        #  Clear the text from each text input

        #  deactivate the inputs
        self.current_equation = None

    def name_text_callback(self, target, value):
        if self.current_equation:
            self.current_equation.update_equation_id(value)

    def equation_text_callback(self, target, value):
        if self.current_equation:
            self.current_equation.set_text(value)

    def insert_equation_name(self, equation):
        #  Do not insert a self reference
        if self.current_equation == equation:
            return

        self.equation_text_editor.delete_selection()
        self.equation_text_editor.insert_text('{delimiter}{equation_id}{delimiter}'.format(
            delimiter=equation.delimiter, equation_id=equation.equation_id
        ))


class EquationScatter(Scatter, Equation):
    output_text = StringProperty("Enter some maths!")

    def __init__(self, blackboard, **kwargs):
        super(EquationScatter, self).__init__(**kwargs)
        super(Equation, self).__init__()

        #  Not sure size hint is used in a float layout
        self.size_hint = (None, None)

        #  The EquationLabel is the display element
        self.equation_label = EquationLabel()

        #  Holds reference to BlackBoard for interface
        self.blackboard = blackboard

        #  Set default properties
        #  Not sure if i used it, but text markup could be interesting
        self.equation_label.markup = True
        self.equation_label.font_size = 20
        self.equation_label.text = "Testing"

        #  Add equation_label so it will display
        self.add_widget(self.equation_label)

        #  Binding to control size of label
        self.equation_label.bind(texture_size=self.label_size_callback)

        #  Binding to set scatter size to the size of the label
        self.equation_label.bind(size=self.scatter_size_callback)

        #  Bind output_text to label text
        self.update_label_text(target=None, value=self.output_text)
        self.bind(output_text=self.update_label_text)

    def update_label_text(self, target, value):
        self.equation_label.text = '({})='.format(self.equation_id) + str(value)

    def label_size_callback(self, target, value):
        self.equation_label.size = value

    def scatter_size_callback(self, target, value):
        self.size = value


class BlackBoard(FloatLayout):

    def __init__(self, name_editor, text_editor, **kwargs):
        super(BlackBoard, self).__init__(**kwargs)
        self.editor = EquationEditor(name_editor, text_editor)

        Clock.schedule_interval(self.draw_callback, 0.2)

#  Draw methods
#  These are the methods used for drawing the arrows or lines to show connections
#  They also make use of the staticmethod process_connections imported from sketchystatic
    def draw_callback(self, dt):
        line_feed = self.generate_list_of_points_to_draw_lines(self.generate_list_of_links())
        self.clear_canvas_for_lines()
        self.feed_list_of_points_to_draw_connection(line_feed)

    def clear_canvas_for_lines(self):
        self.canvas.after.clear()

    def draw_connection(self, points, **kwargs):
        color = [0, 1, 0, .5]

        with self.canvas.after:
            Color(*color)
            Line(points=[points], width=1.0)

    def feed_list_of_points_to_draw_connection(self, line_feed):
        for points in line_feed:
            self.draw_connection(points)

    def generate_list_of_links(self):
        links_list: [(EquationScatter, EquationScatter)]
        links_list = []
        for child in self.children:
            for link in child.links:
                links_list.append((child, child.get_equation(link)))

        return links_list

    def generate_list_of_points_to_draw_lines(self, links_list):
        line_feed = []
        for inst1, inst2 in links_list:
            line_feed.append(process_connections(inst2, inst1))
        return line_feed
#  End draw methods

#  Input controls (mouse commands)
    def on_touch_down(self, touch):
        super(BlackBoard, self).on_touch_down(touch)
        if self.collide_point(*touch.pos):
            for child in self.children:
                if child.collide_point(*touch.pos):
                    if touch.is_double_tap:
                        return False
                    elif touch.button == 'middle':
                        self.editor.insert_equation_name(child)
                        return True
                    elif touch.button == 'scrollup' or touch.button == 'scrolldown':
                        self.scale_single_equation(child, touch.button)
                    else:
                        to_delete = self.editor.change_focus(child)
                        if to_delete:
                            self.delete_equation(to_delete)
                        return True

                #  If touch does not collide with another widget and is double tap create new
            if touch.is_double_tap:
                self.new_equation(touch.pos)
            return True

    def on_touch_up(self, touch):
        super(BlackBoard, self).on_touch_up(touch)
        #  Prevents losing focus from releasing mouse button
        FocusBehavior.ignored_touch.append(touch)

#  Scale, drag, and zoom controls
    @staticmethod
    def scale_single_equation(equation, button):
        if button == 'scrollup':
            equation.scale += .1
        if button == 'scrolldown':
            equation.scale -= .1

    def new_equation(self, pos):
        new_equation = EquationScatter(self)
        new_equation.center = pos
        #  Add to an equation dictionary
        #  Load the Equation TextWidget

        #  Add new equation to blackboard
        self.add_widget(new_equation)

        self.editor.change_focus(new_equation)

    def delete_equation(self, equation=None):
        if equation:
            equation.delete_equation(equation)
            self.remove_widget(equation)
            del equation

    def clear_all(self):
        for child in self.children:
            equation_id = child.equation_id
            child.delete_equation(equation_id)
        self.clear_widgets()

    def load_equation_data(self, data):
        self.clear_all()
        for entry in data:
            if entry['type'] == 'equation':
                new_equation = EquationScatter(self)
                new_equation.update_equation_id(entry['equation_id'])
                new_equation.pos = entry['pos']
                new_equation.equation_text = entry['equation_text']
                new_equation.scale = entry['scale']
                self.add_widget(new_equation)


    def build_save_equation_data(self):
        save_data = []
        for child in self.children:
            new_entry = {}
            new_entry['type'] = 'equation'
            new_entry['equation_id'] = child.equation_id
            new_entry['pos'] = child.pos
            new_entry['equation_text'] = child.equation_text
            new_entry['scale'] = child.scale

            save_data.append(new_entry)

        return save_data


class SketchyMath(BoxLayout):
    previous_equation = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SketchyMath, self).__init__(**kwargs)

        self.orientation = 'vertical'

        # Grid for text inputs
        self.text_editor_box = GridLayout(cols=2)
        self.text_editor_box.size_hint_y = None
        self.text_editor_box.height = 60

        # Labels for text inputs
        self.equation_name_label = GenericLabel()
        self.equation_name_label.text = 'Equation Name'
        self.equation_name_label.size_hint = (.25, .2)
        self.equation_text_label = GenericLabel()
        self.equation_text_label.text = 'Equation'
        self.equation_text_label.size_hint = (.75, .8)

        # Text inputs for name and text of equations
        self.equation_name_editor = EquationTextInput()
        self.equation_name_editor.size_hint_x = .25
        self.equation_text_editor = EquationTextInput()
        self.equation_text_editor.text = ''
        self.equation_text_editor.size_hint_x = .75

        # Blackboard is a float layout that holds the equations
        self.blackboard = BlackBoard(self.equation_name_editor, self.equation_text_editor)

        # Assemble all of the elements together
        self.text_editor_box.add_widget(self.equation_name_label)
        self.text_editor_box.add_widget(self.equation_text_label)
        self.text_editor_box.add_widget(self.equation_name_editor)
        self.text_editor_box.add_widget(self.equation_text_editor)

        self.add_widget(self.text_editor_box)
        self.add_widget(self.blackboard)


class SketchyMathsApp(App):
    def build(self):
        #  Disables multitouch controls
        Config.set('input', 'mouse', 'mouse,disable_multitouch')

        return SketchyMath()


if __name__ == '__main__':
    SketchyMathsApp().run()


