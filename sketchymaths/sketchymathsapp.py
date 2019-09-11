from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty, DictProperty
from sketchymaths import sketchymathmethods
from kivy.uix.settings import SettingsWithTabbedPanel

#  Import internal code from internalsketch
from sketchymaths.internalsketch.sketchysettings import settings_json, settings_defaults
from sketchymaths.internalsketch.sketchyload import SketchyLoad
from sketchymaths.internalsketch.sketchysave import SketchySave
from sketchymaths.internalsketch.sketchyguide import SketchyGuide
import sketchymaths.internalsketch.sketchystatic as ss

#  For debugging
# from sketchymaths.internalsketch.debuggingfuntimes import SketchCollection

class MenuButton(Button):
    def __init__(self, **kwargs):
        super(MenuButton, self).__init__(**kwargs)
        self.font_size = 20

class SketchyMain(Screen):
    def __init__(self, **kwargs):
        super(SketchyMain, self).__init__(**kwargs)
        self.box1 = BoxLayout()
        self.box1.orientation = 'vertical'
        self.maths = SketchyMath(main=self)
        self.maths.name = 'maths'
        self.buttons_box = BoxLayout()
        self.buttons_box.orientation = 'horizontal'
        self.bind(height=self.height_callback)

        self.guide_button = MenuButton()
        self.guide_button.text = 'Guide'
        self.save_button = MenuButton()
        self.save_button.text = 'Save'
        self.load_button = MenuButton()
        self.load_button.text = 'Load'
        self.clear_button = MenuButton()
        self.clear_button.text = 'Clear'
        self.quit_button = MenuButton()
        self.quit_button.text = 'Quit'

        self.buttons_box.add_widget(self.guide_button)
        self.buttons_box.add_widget(self.save_button)
        self.buttons_box.add_widget(self.load_button)
        self.buttons_box.add_widget(self.clear_button)
        self.buttons_box.add_widget(self.quit_button)

        self.box1.add_widget(self.maths)
        self.box1.add_widget(self.buttons_box)

        self.add_widget(self.box1)

        self.guide_button.bind(on_press=self.menu_button_callback)
        self.save_button.bind(on_press=self.menu_button_callback)
        self.load_button.bind(on_press=self.menu_button_callback)
        self.clear_button.bind(on_press=self.menu_button_callback)
        self.quit_button.bind(on_press=self.menu_button_callback)

    def menu_button_callback(self, target):
        if target.text == 'Guide':
            self.screenmanager.current = 'guide'
        elif target.text == 'Save':
            self.screenmanager.current = 'save'
        elif target.text == 'Load':
            self.screenmanager.current = 'load'
        elif target.text == 'Clear':
            self.maths.load_function(data=None)
        elif target.text == 'Quit':
            self.screenmanager.save.auto_save()
            self.screenmanager.app.stop()

    def height_callback(self, target, value):
        self.buttons_box.size_hint_y = 25 / value


class SketchyScreens(ScreenManager):
    def __init__(self, **kwargs):
        super(SketchyScreens, self).__init__(**kwargs)
        self.main = SketchyMain()
        self.main.name = 'main'
        self.guide = SketchyGuide()
        self.guide.name = 'guide'
        self.load = SketchyLoad()
        self.load.name = 'load'
        self.save = SketchySave()
        self.save.main = self
        self.save.name = 'save'

        self.main.screenmanager = self
        self.guide.screenmanager = self
        self.load.screenmanager = self
        self.save.screenmanager = self

        self.add_widget(self.main)
        self.add_widget(self.guide)
        self.add_widget(self.load)
        self.add_widget(self.save)

    def load_data(self, data):
        self.main.maths.load_function(data)

    def save_data(self):
        return self.main.maths.equations


class GenericLabel(Label):
    def __init__(self, **kwargs):
        super(GenericLabel, self).__init__(**kwargs)
        self.font_size = 18
        self.padding_x = 20
        self.bind(size=self.generic_callback)

    def generic_callback(self, target, value):
        self.text_size = value


class EquationEditor(TextInput):
    root = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(EquationEditor, self).__init__(**kwargs)
        self.write_tab = False
        self.bind(focus=self.on_focus)
        self.height = 40
        self.font_size = 20
        self.size_hint_y = None
        self.multiline = False

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if self.focus:
            if self.__name__ == 'eq_text':
                if self.text_selection(keycode):
                    return True
        super(EquationEditor, self).keyboard_on_key_down(window, keycode, text, modifiers)

    def text_selection(self, keycode):
        if 'enter' in keycode:
            cursor_start = self.cursor_index()
            if ':' in self.text:
                i = [self.text.find(':')]
                while i[-1] != -1:
                    i.append(self.text.find(':', i[-1]+1))
                i_zip = [[x, y] for x,y in zip([i[0::2]], [i[1::2]])]
                for x,y in i_zip:
                    for xx,yy in zip(x,y):
                        if cursor_start <= xx and yy != -1:
                            while self.cursor_index() < yy:
                                self.do_cursor_movement('cursor_right')
                            self.cancel_selection()
                            self.select_text(xx, yy+1)
                            return True
                if self.cursor_index() == 0:
                    return True
                else:
                    self.do_cursor_movement('cursor_home')
                    self.text_selection('enter')
            return True
        return False

    def on_focus(self, instance, value, *largs):
        if value:
            Clock.schedule_once(lambda x: self.select_all())


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
        self.size_hint = (None, None)
        self.equationlabel = EquationLabel()
        self.equationlabel.markup = True
        self.equationlabel.font_size = 20
        self.equationlabel.text = 'Type in some maths!'
        self.add_widget(self.equationlabel)
        self.bind(text=self.label_text_callback)
        self.equationlabel.bind(texture_size=self.label_size_callback)
        self.equationlabel.bind(size=self.scatter_size_callback)
        # self.equation_display = Label(font_size=12, color=[1, 0, 0, 1], height=-15)
        # self.add_widget(self.equation_display)
        # self.bind(equation_text=self.equation_display.setter('text'))

    def label_text_callback(self, target, value):
        self.equationlabel.text = value

    def label_size_callback(self, target, value):
        self.equationlabel.size = value

    def scatter_size_callback(self, target, value):
        self.size = value

    def evaluate(self, equation, origin=None, internal=False, depth_counter=0):
        """
        Evaluate equation while replacing references with their target.
        Includes error checking to prevent self referencing.
        If any references reference this equation '(Self)' will be
        displayed.

        If a reference to itself is buried, or it references an equation that already has an unresolved
        infinite loop, the depth_counter will reach the depth_limit,
        and the sources of that limit will change color.

        origin is the original equation when evaluate calls itself
        internal is set to True when evaluate is called inside of itself

        :param depth_counter:
        :param equation: str
        :param origin: object
        :param internal: boolean
        :return:
        """
        depth_limit = int(self.app.config.get('Settings', 'depth_limit'))
        if depth_counter > depth_limit:
            self.evaluation_completed_check('DEPTH_LIMIT')
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
                                                    origin=origin, depth_counter=depth_counter + 1))
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
            self.equationlabel.color = \
                translate_color_config(self.app.config.get('Settings', 'comment_color'))
        elif success == 'DEPTH_LIMIT':
            self.equationlabel.color = \
                translate_color_config(self.app.config.get('Settings', 'depth_limit_color'))
        elif success:
            self.equationlabel.color = \
                translate_color_config(self.app.config.get('Settings', 'text_color_main'))
        elif not success:
            self.equationlabel.color = \
                translate_color_config(self.app.config.get('Settings', 'text_color_faded'))

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
        # if self.focused_text == 'equation_name_editor':
        #     self.root.equation_editor.focus = True
        #     self.root.equation_editor.select_all()
        #     self.focused_text = 'equation_editor'
        #     return
        # if self.focused_text == 'equation_editor':
        #     self.root.equation_name_editor.focus = True
        #     self.root.equation_name_editor.select_all()
        #     self.focused_text = 'equation_name_editor'
        #     return
        if not self.root.equation_editor.focus:
            self.root.equation_editor.focus = True
            self.root.equation_editor.select_all()
        #     self.focused_text = 'equation_editor'

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
    def update_text(self, target=None, value=None):
        self.text = self.evaluate(self.equation_text)

    def on_touch_down(self, touch):
        super(EquationScatter, self).on_touch_down(touch)
        if self.collide_point(*touch.pos):
            if self.root.equation_editor.collide_point(*touch.pos):
                return False
            if touch.button == 'left':
                self.equation_bind()
                self.test_dependencies()
            elif touch.button == 'middle':
                if self != self.root.previous_equation:
                    self.root.equation_editor.delete_selection()
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
        self.update_call = False

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
                        self.unbind_all_equations()
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
        change = 1 + change*0.1
        for equation in self.root.equations.values():
            equation.equationlabel.font_size *= change

            equation.center_x = (equation.center_x - center_point[0])*change
            equation.center_x += center_point[0]
            equation.center_y = (equation.center_y - center_point[1])*change
            equation.center_y += center_point[1]

    def drag_screen(self, dpos):
        self.update_connections(None, None)
        for equation in self.root.equations.values():
            equation.x += dpos[0]
            equation.y += dpos[1]

    def on_touch_up(self, touch, after=False):

        if touch.grab_current is self:
            self.bind_all_equations()
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

    # update_connections, unbind_all_equations, and bind_all_equations:
    # used to reduce lag caused by a large number of updates to draw_connection
    # from things such as dragging or zooming
    def update_connections(self, value=None, target=None):
        if not self.update_call:
            Clock.schedule_once(self.draw_connections, .1)
            self.update_call = True

    def unbind_all_equations(self):
        for inst in self.root.equations.values():
            inst.unbind(x=self.update_connections)

    def bind_all_equations(self):
        for inst in self.root.equations.values():
            inst.bind(x=self.update_connections)

    def draw_connections(self, *args):
        """
        If connections are found, call the draw_connection function with the arguments
        returned by the process_connections function

        :param args:
        :return:
        """

        self.root.clear_connections()
        for inst in self.root.equations.values():
            if '#' in inst.equation_text:
                continue
            for check in self.root.equations.values():
                if '#' in check.equation_text:
                    continue
                if inst != check:
                    if ':%s:' % inst.equation_id in check.equation_text:
                        self.root.draw_connection(ss.process_connections(inst, check))
        self.update_call = False


class SketchyMath(BoxLayout):
    previous_equation = ObjectProperty(None)
    equations = DictProperty()

    def __init__(self, main, **kwargs):
        super(SketchyMath, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.main = main

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
        self.equation_editor.__name__ = 'eq_text'

        self.blackboard = BlackBoard(size=self.size, root=self)

        self.texteditorbox.add_widget(self.equation_name_label)
        self.texteditorbox.add_widget(self.equation_text_label)
        self.texteditorbox.add_widget(self.equation_name_editor,)
        self.texteditorbox.add_widget(self.equation_editor, 0)

        self.add_widget(self.texteditorbox)
        self.add_widget(self.blackboard, canvas='before')

    def auto_save_callback(self, *args):
        self.main.screenmanager.save.auto_save()

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
        eq.app = self.main.screenmanager.app
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
        eq.bind(x=self.blackboard.update_connections)

    def on_touch_down(self, touch):
        super(SketchyMath, self).on_touch_down(touch)
        if self.blackboard.collide_point(*touch.pos):
            if touch.is_double_tap\
                    and touch.button == 'left':
                for inst in self.equations.values():
                    if inst.collide_point(*touch.pos):
                        return
                self.new_equation(touch.pos)

    def bind_equation_to_draw_connections(self, target):
        target.bind(x=self.blackboard.update_connections)

    def draw_connection(self, points, **kwargs):
        """
        Draws a line between two equations with an arrow.
        :param points: x and y coordinates for drawing a line with an arrow
        :param kwargs:
        :return:
        """
        color = \
            translate_color_config(self.main.screenmanager.app.config.get('Settings', 'arrow_color'))
        color.append(self.main.screenmanager.app.config.get('Settings', 'arrow_transparency'))
        with self.canvas.after:
            Color(color[0], color[1], color[2], color[3])
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
                eq.app = self.main.screenmanager.app
                eq.pos = save[1]
                eq.equation_id = str(save[0])
                eq.root = self
                self.equations[str(save[0])] = eq
                self.blackboard.add_widget(eq)
                eq.equation_text = str(save[2])
                eq.equationlabel.font_size = save[3]
        for inst in self.equations.values():
            inst.update_text(target=None)
            self.bind_equation_to_draw_connections(inst)
        self.blackboard.update_connections()

class MySettingsWithTabbedPanel(SettingsWithTabbedPanel):
    pass

def translate_color_config(color_string: str):
    x = color_string.split(',')
    y = []
    for i in range(len(x)):
        y.append(float(x[i]))
    return y


class SketchyMathsApp(App):

    def build(self):
        self.settings_cls = MySettingsWithTabbedPanel
        self.root = SketchyScreens()
        self.root.app = self
        self.root.auto_save_clock = \
            Clock.schedule_interval(self.root.main.maths.auto_save_callback,
                                    int(self.root.app.config.get('Settings', 'auto_save_interval')) * 60)
        return self.root

    #  Settings data is imported as settings_json and settings_default from sketchysettings.py
    def build_config(self, config):
        config.setdefaults('Settings', settings_defaults)

    def build_settings(self, settings):
        settings.add_json_panel('Settings', self.config, data=settings_json)

    def on_config_change(self, config, section, key, value):
        if section == 'Settings':
            if key == 'auto_save_interval':
                self.root.auto_save_clock = Clock.schedule_interval(self.root.main.maths.auto_save_callback,
                                                                    int(value)*60)

    def close_settings(self, settings=None, *largs):
        super(SketchyMathsApp, self).close_settings(settings)
        for equation in self.root.main.maths.equations.values():
            equation.update_text()
        self.root.main.maths.blackboard.update_connections()

