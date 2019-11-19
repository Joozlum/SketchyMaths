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
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty

from internalsketch.sketchysettings import behavior_settings_defaults, appearance_settings_defaults, \
    behavior_settings_json, appearance_settings_json
from sketchymaths import sketchymathmethods
from kivy.config import Config

#  Import internal code from internalsketch
from sketchymaths.internalsketch.sketchyload import SketchyLoad
from sketchymaths.internalsketch.sketchysave import SketchySave
from sketchymaths.internalsketch.sketchyguide import SketchyGuide
from sketchymaths.internalsketch.equations import Equation
import sketchymaths.internalsketch.sketchystatic as ss


#  For debugging
# from sketchymaths.internalsketch.debuggingfuntimes import SketchCollection


# todo
#   create settings screen

class MenuButton(Button):
    def __init__(self, **kwargs):
        super(MenuButton, self).__init__(**kwargs)
        self.font_size = 20

class SketchyMain(Screen):
    def __init__(self, get_setting, **kwargs):
        super(SketchyMain, self).__init__(**kwargs)
        self.box1 = BoxLayout()
        self.box1.orientation = 'vertical'
        self.maths = SketchyMath(main=self, get_setting=get_setting)
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
            self.maths.blackboard.clear_all()
        elif target.text == 'Quit':
            self.screenmanager.save.auto_save()
            self.screenmanager.app.stop()

    def height_callback(self, target, value):
        self.buttons_box.size_hint_y = 25 / value


class SketchyScreens(ScreenManager):
    def __init__(self, app, **kwargs):
        super(SketchyScreens, self).__init__(**kwargs)

        # holds link to app so it can call for stop()
        self.app = app

        self.main = SketchyMain(self.app.config.get)
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
        self.main.maths.blackboard.load_equation_data(data)

    def save_data(self):
        return self.main.maths.blackboard.build_save_equation_data()

    def auto_save_callback(self, *args):
        self.save.auto_save()


class GenericLabel(Label):
    def __init__(self, **kwargs):
        super(GenericLabel, self).__init__(**kwargs)
        self.font_size = 18
        self.padding_x = 20
        self.bind(size=self.generic_callback)

    def generic_callback(self, target, value):
        self.text_size = value


class EquationTextInput(TextInput):
    root = ObjectProperty(None)

    def __init__(self, name, **kwargs):
        super(EquationTextInput, self).__init__(**kwargs)
        self.name = name
        self.write_tab = False
        self.bind(focus=self.on_focus)
        self.height = 40
        self.font_size = 20
        self.size_hint_y = None
        self.multiline = False

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if self.focus:
            if self.name == 'text_editor':
                if self.text_selection(keycode):
                    return True
        super(EquationTextInput, self).keyboard_on_key_down(window, keycode, text, modifiers)

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

    def change_focus(self, equation):
        to_delete = None
        if self.current_equation:
            if self.current_equation.equation_text == '':
                to_delete = self.current_equation

        #  Only run if equation is different
        if self.current_equation is not equation:
            self.current_equation = equation
            self.equation_name_editor.text = equation.equation_id
            self.equation_text_editor.text = f'{equation.equation_text}'

        self.equation_text_editor.focus = True
        Clock.schedule_once(lambda x: self.equation_text_editor.select_all())
        return to_delete

    def clear_focus(self):
        self.current_equation = None
        self.equation_text_editor.text = ''
        self.equation_name_editor.text = ''

    def name_text_callback(self, target, value):
        if self.current_equation:
            self.current_equation.update_equation_id(value)
            self.current_equation.update_label_text()

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
        self.update_label_text()
        self.bind(output_text=self.update_label_text)

    def update_label_text(self, target=None, value=None):

        #  This allows for calling with no parameters for updating display
        if value is None:
            value = self.output_text

        #  Change display of comments
        if '#' in value:
            #  call settings to get color value, then translate it
            comment_color = self.blackboard.get_setting('Appearance', 'comment_color')
            self.equation_label.color = ss.translate_color_config(comment_color)

            self.equation_label.text = str(value)

        #  Run for if evaluate was successful
        elif self.status:
            color = self.blackboard.get_setting('Appearance', 'text_color_main')
            self.equation_label.color = ss.translate_color_config(color)

            #  if float round number to x decimal places from settings
            #  this only affects display, as it does not alter the stored value
            if self.type == float:
                decimal_places = self.blackboard.get_setting('Behavior', 'decimal_places')
                formatting = f'{{:.{int(decimal_places)}f}}'
                value = formatting.format(float(value))

            self.equation_label.text = f'({self.equation_id})={value}'

        #  Run for when evaluation was unsuccessful, and display error message
        else:
            color = self.blackboard.get_setting('Appearance', 'text_color_faded')
            self.equation_label.color = ss.translate_color_config(color)
            self.equation_label.text = f'({self.equation_id})={value}'
            if self.error:
                self.equation_label.text += f'\n[size=10]{self.error}[/size]'

    def label_size_callback(self, target, value):
        self.equation_label.size = value

    def scatter_size_callback(self, target, value):
        self.size = value

class BlackBoard(FloatLayout):

    def __init__(self, name_editor, text_editor, get_setting, **kwargs):
        super(BlackBoard, self).__init__(**kwargs)
        self.editor = EquationEditor(name_editor, text_editor)

        #  method for calling for a settings value
        self.get_setting = get_setting

        #  update interval for drawing arrows
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
        color = ss.translate_color_config(self.get_setting('Appearance', 'arrow_color'))
        color.append(self.get_setting('Appearance', 'arrow_transparency'))

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
            line_feed.append(ss.process_connections(inst2, inst1))
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
                        #  pass equation for text focus and capture to_delete
                        to_delete = self.editor.change_focus(child)
                        if to_delete:
                            self.delete_equation(to_delete)
                        return True

            #  If touch does not collide with another widget and is double tap create new
            if touch.is_double_tap:
                self.new_equation(touch.pos)
                return True
            if touch.button == 'left':
                touch.grab(self)
                return True
            if touch.button == 'scrollup':
                self.zoom(touch.pos, -1)
                return True
            if touch.button == 'scrolldown':
                self.zoom(touch.pos, 1)
                return True

    def on_touch_up(self, touch):
        super(BlackBoard, self).on_touch_up(touch)
        #  Prevents losing focus from releasing mouse button
        FocusBehavior.ignored_touch.append(touch)

        #  If self is grabbed then ungrab
        if touch.grab_current is self:
            touch.ungrab(self)

    def on_touch_move(self, touch):
        """
            If self is grabbed then run drag_screen
        :param touch:
        :return:
        """
        if touch.grab_current is self:
            self.drag_screen(touch.dpos)
        else:
            return

#  Scale, drag, and zoom controls
    @staticmethod
    def scale_single_equation(equation, button):
        if button == 'scrollup':
            equation.scale += .1
        if button == 'scrolldown':
            equation.scale -= .1

    def drag_screen(self, dpos):
        for child in self.children:
            child.x += dpos[0]
            child.y += dpos[1]

    def zoom(self, center_point, change):
        change = 1 + change*0.1
        for child in self.children:
            child.scale *= change

            child.center_x = (child.center_x - center_point[0])*change
            child.center_x += center_point[0]
            child.center_y = (child.center_y - center_point[1])*change
            child.center_y += center_point[1]

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
        self.editor.clear_focus()

    def load_equation_data(self, data):
        self.clear_all()
        for entry in data:
            if entry['type'] == 'equation':
                new_equation = EquationScatter(self)
                new_equation.update_equation_id(entry['equation_id'])
                new_equation.equation_text = entry['equation_text']
                new_equation.links = entry['links']
                for ref in entry['references']:
                    new_equation.add_reference(ref)
                self.add_widget(new_equation)
                new_equation.scale = entry['scale']  # scale needs to be loaded before pos
                new_equation.pos = entry['pos']
        for child in self.children:
            child.set_text()

    def build_save_equation_data(self):
        save_data = []
        for child in self.children:
            new_entry = {}
            new_entry['type'] = 'equation'
            new_entry['equation_id'] = child.equation_id
            new_entry['pos'] = child.pos
            new_entry['equation_text'] = child.equation_text
            new_entry['scale'] = child.scale
            new_entry['links'] = child.links
            new_entry['references'] = child.get_references()

            save_data.append(new_entry)

        return save_data


class SketchyMath(BoxLayout):

    def __init__(self, main, get_setting, **kwargs):
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
        self.equation_name_editor = EquationTextInput(name='name_editor')
        self.equation_name_editor.size_hint_x = .25
        self.equation_text_editor = EquationTextInput(name='text_editor')
        self.equation_text_editor.text = ''
        self.equation_text_editor.size_hint_x = .75

        # Blackboard is a float layout that holds the equations
        # A reference of the two text editors is passed to the Blackboard here,
        # so it can interact with them.
        self.blackboard = BlackBoard(self.equation_name_editor, self.equation_text_editor, get_setting)

        # Assemble all of the elements together
        self.text_editor_box.add_widget(self.equation_name_label)
        self.text_editor_box.add_widget(self.equation_text_label)
        self.text_editor_box.add_widget(self.equation_name_editor)
        self.text_editor_box.add_widget(self.equation_text_editor)

        self.add_widget(self.text_editor_box)
        #  canvas='before' ensures TextInputs are drawn on top layer
        self.add_widget(self.blackboard, canvas='before')


class SketchyMathsApp(App):

    def build(self):
        #  Disables multi-touch
        Config.set('input', 'mouse', 'mouse,disable_multitouch')

        #  Initialize settings panel
        self.settings_cls = MySettingsWithTabbedPanel
        self.root = SketchyScreens(app=self)
        self.root.app = self  # reference added here so SketchyScreens can call stop()

        self.root.auto_save_clock = Clock.schedule_interval(
            self.root.auto_save_callback,
            int(self.root.app.config.get('Behavior', 'auto_save_interval')) * 60)

        return self.root

    #  building settings panel
    def build_config(self, config):
        config.setdefaults('Behavior', behavior_settings_defaults)
        config.setdefaults('Appearance', appearance_settings_defaults)

    def build_settings(self, settings):
        settings.add_json_panel('Behavior', self.config, data=behavior_settings_json)
        settings.add_json_panel('Appearance', self.config, data=appearance_settings_json)

    def on_config_change(self, config, section, key, value):
        if section == 'Behavior':
            if key == 'auto_save_interval':
                self.root.auto_save_clock = Clock.schedule_interval(
                    self.root.auto_save_callback,
                    int(value)*60
                )

#  Class for settings panel
class MySettingsWithTabbedPanel(SettingsWithTabbedPanel):
    pass
