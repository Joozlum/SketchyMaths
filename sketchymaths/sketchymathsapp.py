from math import atan2, cos, sin
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty, DictProperty
from sketchymaths import sketchymathmethods, sketchyload, sketchysave

#  Disable multitouch
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch')

DEPTH_LIMIT = 30


class SketchyMain(Screen):
    pass


class SketchyGuide(Screen):
    pass


class SketchyScreens(ScreenManager):
    def load_data(self, data):
        self.get_screen('main').children[0].children[1].load_function(data)

    def save_data(self):
        return self.get_screen('main').children[0].children[1].equations


class GenericLabel(Label):
    pass


class EquationEditor(TextInput):
    root = ObjectProperty(None)


class EquationLabel(Label):
    def on_parent(self, widget, parent):
        parent.equationlabel = self


class EquationScatter(Scatter):
    equation_text = StringProperty('Click me and type above!')
    root = ObjectProperty(None)
    equation_id = StringProperty('')
    text = StringProperty('Click me and type above!')
    focused_text = ''
    equationlabel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(EquationScatter, self).__init__(**kwargs)
        self.fbind('equation_text', self.update_text)
        # self.equation_display = Label(font_size=12, color=[1, 0, 0, 1], height=-15)
        # self.add_widget(self.equation_display)
        # self.bind(equation_text=self.equation_display.setter('text'))

    def evaluate(self, equation, origin=None, internal=False, depth_limit=0):
        """
        Evaluate equation while replacing references with their target.
        Includes error checking to prevent self referencing.
        If any references reference this equation '(Self)' will be
        displayed.

        origin is the original equation when evaluate calls itself
        internal is set to True when evaluate is called inside of itself

        :param depth_limit:
        :param equation: str
        :param origin: object
        :param internal: boolean
        :return:
        """
        if depth_limit > DEPTH_LIMIT:
            return '*DEPTH_LIMIT*'
        if '#' in equation:
            self.evaluation_completed_check('comment')
            return equation

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
                                                    origin=origin, depth_limit=depth_limit+1))
                else:
                    equation = equation.replace(":%s:" % key, "(Self)")
        #  evaluate the equation
        try:
            result = str(eval(equation, {'__builtins__': None}, sketchymathmethods.sketchy_dict))
            success = True
        except:
            result = equation
            success = False
        if internal:
            if success:
                return result
            if not success:
                return self.equation_id

        self.evaluation_completed_check(success)
        return "(%s)= %s" % (self.equation_id, result)

    def evaluation_completed_check(self, success):
        if success == 'comment':
            self.equationlabel.color = (0, .8, 1)
        elif success:
            self.equationlabel.color = (1, 1, 1)
        elif not success:
            self.equationlabel.color = (.5, .5, .5)

    #  Run a dependency test as well as the binding callback
    def test_dependencies(self, internal=False, previous=None):

        for inst in self.root.equations.values():
            for check in self.root.equations.values():
                if inst != check:
                    if ':%s:' % inst.equation_id in check.equation_text:
                        #  in every check see if inst is referenced
                        inst.bind(text=check.update_text)

    def dependency_clear(self):
        pass

    #  Used on_touch_up to select all text in equation_editor
    #  or all text in equation name editor and set keyboard focus
    def text_editor_focus_control(self, target=None, value=None):
        if self.focused_text == 'equation_name_editor':
            self.root.equation_editor.focus = True
            self.root.equation_editor.select_all()
            self.focused_text = 'equation_editor'
            return
        if self.focused_text == 'equation_editor':
            self.root.equation_name_editor.focus = True
            self.root.equation_name_editor.select_all()
            self.focused_text = 'equation_name_editor'
            return
        self.root.equation_editor.focus = True
        self.root.equation_editor.select_all()
        self.focused_text = 'equation_editor'

    #  Bind EquationEditor to callback text_focus
    def equation_bind(self):
        if self.root.previous_equation is not None:
            self.root.equation_editor.funbind('text', self.root.previous_equation.text_focus)
            self.root.equation_name_editor.funbind('text', self.root.previous_equation.id_text_focus)
            if self.root.previous_equation != self:
                self.root.previous_equation.focused_text = 'None'
            self.root.previous_equation.equationlabel.bold = False

        #  Set EquationEditor text to focused equation and bind them
        self.root.equation_editor.text = self.equation_text
        self.root.equation_editor.fbind('text', self.text_focus)

        #  Set id Editor text to focused equation's id and bind them
        self.root.equation_name_editor.text = str(self.equation_id)
        self.root.equation_name_editor.fbind('text', self.id_text_focus)

        #  if previous_equation is empty then call for deletion
        if self.root.previous_equation is not None:
            if self.root.previous_equation.equation_text == 'empty':
                self.root.delete_equation()

        self.root.previous_equation = self
        self.equationlabel.bold = True

    #  Callback for binding equation_editor text to equation_text
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
            if touch.button == 'left':
                self.equation_bind()
                self.test_dependencies()
            elif touch.button == 'middle':
                if self != self.root.previous_equation:
                    self.root.equation_editor.insert_text(':{id}:'.format(id=self.equation_id))
            elif touch.button == 'scrollup' or touch.button == 'scrolldown':
                self.text_size_change(self, touch.button)
                return True

    #  Adjust size of equationlabel
    def text_size_change(self, target, value):
        if value == "scrollup"\
                and target.equationlabel.font_size > 8:
            self.change_font_size(-1)
        elif value == "scrolldown":
            self.change_font_size(1)

    #  Scales font size around center of equation position, rather than from bottom left corner
    def change_font_size(self, change):
        original_center = self.center
        self.equationlabel.font_size += change
        self.equationlabel.texture_update()
        self.center = original_center

    #  Callback for binding equation_name_editor to equation_id
    def id_text_focus(self, target, value=None):
        self.update_equation_id(target.text)
        self.update_text(None)  # update its own text so new id is displayed

    def update_equation_id(self, new_id):
        """
        Updates equations dictionary to reflect new equation_id
        If empty returns without changing
        If a colon is in the name it replaces it with a semi-colon to prevent errors in evaluate
        :type new_id: str
        """
        if new_id == '':
            return
        if ':' in new_id:
            new_id = new_id.replace(":", ";")

        if new_id in self.root.equations:
            return
        if self.equation_id in self.root.equations:
            del self.root.equations[self.equation_id]
        self.root.equations[new_id] = self
        self.update_equation_id_dependencies(self.equation_id, new_id)
        self.equation_id = new_id

    def update_equation_id_dependencies(self, old_id, new_id):
        old_id = ':{old_id}:'.format(old_id=old_id)
        new_id = ':{new_id}:'.format(new_id=new_id)
        for inst in self.root.equations.values():
            if old_id in inst.equation_text:
                inst.equation_text = inst.equation_text.replace(old_id, new_id)


class BlackBoard(FloatLayout):
    root = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(BlackBoard, self).__init__(**kwargs)

    #  For capturing middle mouse button
    def on_touch_down(self, touch, after=False):
        if self.collide_point(*touch.pos):
            if after:
                if touch.button == 'middle':
                    FocusBehavior.ignored_touch.append(touch)
                if touch.button == 'scrollup' or touch.button == 'scrolldown'\
                        or touch.button == 'left':
                    for equation in self.root.equations.values():
                        if equation.collide_point(*touch.pos):
                            return
                    if touch.button == 'scrollup':
                        self.zoom(touch.pos, -1)
                    if touch.button == 'scrolldown':
                        self.zoom(touch.pos, 1)
                    if touch.button == 'left':
                        touch.grab(self)
                return
            else:
                Clock.schedule_once(lambda dt: self.on_touch_down(touch, True))
        return super(BlackBoard, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.drag_screen(touch.dpos)
        else:
            return

    def zoom(self, center_point, change):
        for equation in self.root.equations.values():
            x = (equation.center_x - center_point[0]) * (1 + change * 0.1)
            y = (equation.center_y - center_point[1]) * (1 + change * 0.1)
            equation.center = (x + center_point[0], y + center_point[1])
            f = (equation.equationlabel.font_size * (change*0.1))
            equation.equationlabel.font_size += f

    def drag_screen(self, dpos):
        for equation in self.root.equations.values():
            equation.x += dpos[0]
            equation.y += dpos[1]

    #  Switches focus to EquationEditor or to IDEditor for smoother use
    def on_touch_up(self, touch, after=False):

        if touch.grab_current is self:
            touch.ungrab(self)

        #  If there is a previous_equation, and the previous equation is the current one
        if self.root.previous_equation is not None \
                and self.root.previous_equation.collide_point(*touch.pos)\
                and touch.button == 'left':
            if after:
                self.root.previous_equation.text_editor_focus_control()
                return
            else:
                Clock.schedule_once(lambda dt: self.on_touch_up(touch, True))
        return super(BlackBoard, self).on_touch_up(touch)

    def draw_connections(self, *args):
        """
        If connections are found, call the draw_connection function with the arguments
        returned by the process_connections function

        :param args:
        :return:
        """
        self.root.clear_connections()
        for inst in self.root.equations.values():
            for check in self.root.equations.values():
                if inst != check:
                    if ':%s:' % inst.equation_id in check.equation_text:
                        self.root.draw_connection(self.process_connections(inst, check))

    def process_connections(self, inst1, inst2):
        """
        Takes in two instances and using their position properties determines what
        points to use to draw a line between them along with an arrow

        :param inst1:
        :param inst2:
        :return: List of points to draw a line through
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
        ax = -15 * cos(angle + .3) + x2
        ay = -15 * sin(angle + .3) + y2
        bx = -15 * cos(angle - .3) + x2
        by = -15 * sin(angle - .3) + y2

        return x1, y1, x2, y2, ax, ay, bx, by, x2, y2


class SketchyMath(BoxLayout):
    previous_equation = ObjectProperty(None)
    equations = DictProperty()

    def __init__(self, **kwargs):
        super(SketchyMath, self).__init__(**kwargs)

        self.texteditorbox = GridLayout(cols=2)
        self.texteditorbox.size_hint_y = None
        self.texteditorbox.height = 60

        self.equation_name_label = GenericLabel()
        self.equation_name_label.text = 'Equation Name:'
        self.equation_name_label.size_hint = (.25, .2)

        self.equation_text_label = GenericLabel()
        self.equation_text_label.text = 'Equation:'
        self.equation_text_label.size_hint = (.75, .8)

        self.equation_name_editor = EquationEditor()
        self.equation_name_editor.root = self
        self.equation_name_editor.text = ''
        self.equation_name_editor.size_hint_x = .25

        self.equation_editor = EquationEditor(root=self)
        self.equation_editor.size_hint_x = .75

        self.blackboard = BlackBoard(size=self.size, root=self)

        self.texteditorbox.add_widget(self.equation_name_label)
        self.texteditorbox.add_widget(self.equation_text_label)
        self.texteditorbox.add_widget(self.equation_name_editor)
        self.texteditorbox.add_widget(self.equation_editor)

        self.add_widget(self.texteditorbox)
        self.add_widget(self.blackboard)

        #  calls function to draw lines four times a second
        Clock.schedule_interval(self.blackboard.draw_connections, 0.25)

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
        ii = 'x' + str(i)
        while ii in self.equations:
            i += 1
            ii = 'x' + str(i)
        else:
            self.equations[ii] = eq
        eq.equation_id = ii
        self.blackboard.add_widget(eq)

        #  Bind new equation to EquationEditor
        eq.equation_bind()

    def on_touch_down(self, touch):
        super(SketchyMath, self).on_touch_down(touch)
        if self.blackboard.collide_point(*touch.pos):
            if touch.is_double_tap\
                    and touch.button == 'left':
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
        key = str(self.previous_equation.equation_id)
        if key in self.equations:
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
                eq.equation_id = str(save[0])
                eq.root = self
                self.equations[str(save[0])] = eq
                self.blackboard.add_widget(eq)
                eq.equation_text = str(save[2])
                eq.equationlabel.font_size = save[3]
        for inst in self.equations.values():
            inst.update_text(target=None)


class SketchyMathsApp(App):

    def build(self):
        return self.root

