import datetime
import json
import pickle
import shelve
from math import atan2, cos, sin

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, DictProperty
from sketchymaths import sketchymathmethods, sketchyload, sketchysave


class SketchyMain(Screen):
    pass


class SketchyGuide(Screen):
    pass


class SketchyScreens(ScreenManager):
    def load_data(self, data):
        self.get_screen('main').children[0].children[1].load_function(data)

    def save_data(self):
        return self.get_screen('main').children[0].children[1].equations


class EquationEditor(TextInput):
    root = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(EquationEditor, self).__init__(**kwargs)
        self.bind(on_text_validate=self.on_enter)

    def on_enter(self, *args):
        #  todo
        #   send command to update all equations
        pass


class EquationLabel(Label):
    pass


class EquationScatter(Scatter):
    equation_text = StringProperty('Click me and type above!')
    root = ObjectProperty(None)
    equation_id = NumericProperty(0)
    text = StringProperty('Click me and type above!')

    def __init__(self, **kwargs):
        super(EquationScatter, self).__init__(**kwargs)
        self.fbind('equation_text', self.update_text)
        self.equation_display = Label(font_size=12, color=[1, 0, 0, 1], height=-15)
        self.add_widget(self.equation_display)
        self.bind(equation_text=self.equation_display.setter('text'))

    def evaluate(self, equation, origin=None, internal=False):
        """
        Evaluate equation while replacing references with their target.
        Includes error checking to prevent self referencing.
        If any references reference this equation '(Self)' will be
        displayed.

        :param equation:
        :param origin:
        :param internal:
        :return:
        """
        if not internal:
            origin = self

        #  replace references before evaluating
        for key in self.root.equations:
            if ":%s:" % key in equation:
                if self.root.equations[key] != self \
                        and origin != self.root.equations[key]:
                    equation = equation.replace(":%s:" % key,
                                                "(%s)" % self.root.equations[key].evaluate(
                                                    self.root.equations[key].equation_text, internal=True,
                                                    origin=origin))
                else:
                    equation = equation.replace(":%s:" % key, "(Self)")
        #  evaluate the equation
        try:
            result = str(eval(equation, {'__builtins__': None}, sketchymathmethods.sketchy_dict))
        except:
            result = equation
        if internal:
            return result
        return "f(%s)= %s" % (self.equation_id, result)

    #  Run a dependency test as well as the binding callback
    #  todo
    #   Clean up this code to make sure it isn't creating
    #   duplicate dependencies.
    def test_dependencies(self, internal=False, previous=None):

        for inst in self.root.equations.values():
            for check in self.root.equations.values():
                if inst != check:
                    if ':%s:' % inst.equation_id in check.equation_text:
                        #  in every check see if inst is referenced
                        inst.bind(text=check.update_text)

    def dependency_clear(self):
        pass

    #  Bind EquationEditor to callback text_focus
    def equation_bind(self):
        if self.root.previous_equation is not None:
            self.root.ET.funbind('text', self.root.previous_equation.text_focus)
            self.root.previous_equation.children[1].bold = False
        self.root.ET.text = self.equation_text
        self.root.ET.fbind('text', self.text_focus)

        #  if previous_equation is empty then call for deletion
        if self.root.previous_equation is not None:
            if self.root.previous_equation.equation_text == 'empty':
                self.root.delete_equation()

        self.root.previous_equation = self
        self.children[1].bold = True

    #  Callback for binding EquationEditor text to equation text
    def text_focus(self, target, value=None):
        if target.text == '':
            self.equation_text = 'empty'  # Display empty if text is blank
        else:
            self.equation_text = target.text

    #  Callback for update_dependencies
    def update_text(self, target, value=None):
        self.text = self.evaluate(self.equation_text)

    def on_touch_down(self, touch):
        super(EquationScatter, self).on_touch_down(touch)
        if self.collide_point(*touch.pos):
            self.equation_bind()
            self.test_dependencies()


class BlackBoard(FloatLayout):
    root = ObjectProperty(None)

    #  Switches focus to EquationEditor for smoother use
    #  todo
    #   Fix how this gets called, as it is calling it twice each time
    def on_touch_up(self, touch, after=False):
        if after:
            if self.root.previous_equation is not None \
                    and self.root.previous_equation.collide_point(*touch.pos):
                self.root.ET.focus = True
                self.root.ET.select_all()

        else:
            Clock.schedule_once(lambda dt: self.on_touch_up(touch, True))
            return super(BlackBoard, self).on_touch_up(touch)

    def draw_connections(self, *args):
        """
        If connections are found, call the draw_connection function to draw a line

        :param args:
        :return:
        """
        self.root.clear_connections()
        for inst in self.root.equations.values():
            for check in self.root.equations.values():
                if inst != check:
                    if ':%s:' % inst.equation_id in check.equation_text:
                        # self.root.draw_connection(first_point=inst.center, second_point=check.center)
                        self.root.draw_connection(self.process_connections(inst, check))

    def process_connections(self, inst1, inst2):
        """
        Takes in two instances and using their position properties determines what
        points to send to the draw_connection function

        :param inst1:
        :param inst2:
        :return:
        """
        x_change = inst2.center_x - inst1.center_x
        y_change = inst2.center_y - inst1.center_y
        if abs(x_change) > abs(y_change):
            y1 = inst1.center_y
            y2 = inst2.center_y
            if x_change > 0:
                x1 = inst1.right
                x2 = inst2.x
            else:
                x1 = inst1.x
                x2 = inst2.right
        else:
            x1 = inst1.center_x
            x2 = inst2.center_x
            if y_change > 0:
                y1 = inst1.top
                y2 = inst2.y
            else:
                y1 = inst1.y
                y2 = inst2.top

        #  calculating points to create arrow:
        x0 = x2 - x1
        y0 = y2 - y1
        angle = atan2(y0, x0)
        ax = -10 * cos(angle + .3) + x2
        ay = -10 * sin(angle + .3) + y2
        bx = -10 * cos(angle - .3) + x2
        by = -10 * sin(angle - .3) + y2

        return x1, y1, x2, y2, ax, ay, bx, by, x2, y2


class SketchyMath(BoxLayout):
    previous_equation = ObjectProperty(None)
    equations = DictProperty()

    def __init__(self, **kwargs):
        super(SketchyMath, self).__init__(**kwargs)
        self.ET = EquationEditor(root=self)
        self.add_widget(self.ET)
        self.blackboard = BlackBoard(size=self.size, root=self)
        self.add_widget(self.blackboard)
        Clock.schedule_interval(self.blackboard.draw_connections, 0.5)

    def new_equation(self, pos, **kwargs):
        """
        Create a new equation at pos (off-self slightly so it appears under the
        mouse/touch that created it.

        :param pos:
        :param kwargs:
        :return:
        """
        eq = EquationScatter(pos=(pos[0] - 20, pos[1] - 10),
                             root=self)
        i = 0
        while i in self.equations:
            i += 1
        else:
            self.equations[i] = eq
        eq.equation_id = i
        self.blackboard.add_widget(eq)

        #  Bind new equation to EquationEditor
        eq.equation_bind()

    def on_touch_down(self, touch):
        super(SketchyMath, self).on_touch_down(touch)
        if self.blackboard.collide_point(*touch.pos):
            if touch.is_double_tap:
                for inst in self.equations.values():
                    if inst.collide_point(*touch.pos):
                        return
                self.new_equation(touch.pos)

    def draw_connection(self, points, **kwargs):
        """
        Draws a line between two equations with an arrow.
        :param points: x and y coordinates for drawing a line with an arrow
        :param kwargs:
        :return:
        """
        with self.canvas.after:
            Color(0, 1, 0, .5)
            Line(points=[points], width=1.0)

    def clear_connections(self):
        self.canvas.after.clear()

    def delete_equation(self):
        key = self.previous_equation.equation_id
        uid = self.equations[key]
        del self.equations[key]
        self.blackboard.remove_widget(uid)


    def load_function(self, data):
        if self.equations is not None:
            for inst in self.equations.values():
                self.blackboard.remove_widget(inst)
        self.equations.clear()

        if data is not None:
            for save in data:
                eq = EquationScatter()
                eq.pos = save[1]
                eq.equation_id = save[0]
                eq.root = self
                self.equations[save[0]] = eq
                self.blackboard.add_widget(eq)
                eq.equation_text = str(save[2])
        for inst in self.equations.values():
            inst.update_text(target=None)


class SketchyMathsApp(App):
    """Basic kivy app

    Edit sketchymaths.kv to get started.
    """

    def build(self):
        return self.root

