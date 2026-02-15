# ##############
# ### Widget ###
# ##############

# This is the main class for the `Widget` type.  
# It offers the following functions, classes & variables to all future Widgets:

#  - **TODO**: write list


# ### Imports ###

import curses
from dataclasses import dataclass

from boxes_tui.shared_vars import SHARED_VARS
from boxes_tui.inputs import KeybindList
from boxes_tui.exceptions import *
from boxes_tui.looks import FormattedText, format_text
from boxes_tui.logger import LogLevel, log

# ### Settings ###

@dataclass
class WidgetSetting:
    has_components:bool = False,
    has_multiple_components:bool = False,
    can_scroll:bool = False,
    has_optional_scroll:bool = False,
    has_selected_components:bool = False,

    default_wanted_width:int = -1,
    default_wanted_height:int = -1,

    can_tick:bool = False,                                # if this widget has components, that can tick, you usually don't want to set this to False, see vv
    has_optional_ticking:bool = False,                    # You usually don't want this, as `can_tick = False` keeps components from ticking too; my_widget.tick() runs my_widget.component(s).tick()
    has_keybinds:bool = False,                            # This will be set to True if the Widget has a `default_keybinds` attibute
    default_keybinds:KeybindList = KeybindList(),         # This will be set to `default_keybinds` if the Widget has that as an attibute

    has_optional_colour:bool = False,
    has_text:bool = False,
    default_show_selected:bool = False,
    has_formatting:bool = False                           # FIXME: What is this meant to do? Maybe if format_text should be called?


# ### Infos ###

@dataclass
class WidgetInformation:
    has_components = False
    has_multiple_components = False
    can_scroll = False
    has_selected_components = False

    has_keybinds = False
    can_tick = False


# ### Results ###

@dataclass
class WidgetTickResult:
    widget_id:str
    keypress:int
    selected_component:int=None

@dataclass
class FunctionTickResult:
    return_value=None


# ### Main class ###

class Widget:
    widget_type = "<Typename not set>"

    #-#-#-# INIT #-#-#-#
    def __init__(
            self,
            widget_id:str=None,
            window=None,
            x_offset:int=0,
            y_offset:int=0,
            **more_args
        ) -> None:

        self.infos = WidgetInformation()

        ## Misc ##
        self.is_selected = False
        if widget_id is None:
            self.widget_id = f'[{type(self).widget_type}]'
        else:
            self.widget_id = widget_id
        if self.widget_id != f'[{type(self).widget_type}]':
            if self.widget_id in SHARED_VARS["WIDGETS"].keys():
                raise BoxesTUI_LibraryUsageError(f'[{self.widget_type}]: ID "{self.widget_id}" defined twice!')
            SHARED_VARS["WIDGETS"][self.widget_id] = self
        self.x_offset = x_offset
        self.y_offset = y_offset

        self.width = 1
        self.height = 1

        self.selected = 0
        self.scroll = 0


        ## Load values ##
        if hasattr(self, 'default_keybinds'):
            if hasattr(self, 'settings'): self.keybinds = more_args.get('keybinds', self.default_keybinds)
            else: self.keybinds = self.default_keybinds

        if hasattr(self, 'settings'):
            # Components
            self.infos.has_components = self.settings.has_components
            if self.settings.has_components:

                self.infos.has_multiple_components = self.settings.has_multiple_components
                if self.settings.has_multiple_components: components = more_args.get('components', [])   # Components = [(widget, function)]
                else:                                     components = [more_args.get('component', None)]

                self.components = []
                for index in range(len(components)):
                    if isinstance(components[index], tuple):
                        self.components.append(components[index])
                    else:
                        self.components.append((components[index], None))

                if self.settings.can_scroll:
                    if self.settings.has_optional_scroll: self.can_scroll = more_args.get('can_scroll', False)
                    else:                                 self.can_scroll = True
                else:
                    self.can_scroll = False
                self.infos.can_scroll = self.can_scroll

                self.infos.has_selected_components = self.settings.has_selected_components
                if self.settings.has_selected_components:
                    self.selected = more_args.get('selected', 0)
                    self.show_selected = more_args.get('show_selected', self.settings.default_show_selected)
                else:
                    self.selected = 0
                    self.show_selected = False

            # Size
            if not (self.settings.default_wanted_width is None): self.wanted_width = more_args.get('wanted_width', self.settings.default_wanted_width)
            if not (self.settings.default_wanted_height is None): self.wanted_height = more_args.get('wanted_height', self.settings.default_wanted_height)

            # Keybinds & Ticking
            self.can_tick = self.settings.can_tick
            if self.settings.can_tick:
                if self.settings.has_optional_ticking: self.can_tick = more_args.get('can_tick', True)
                else: self.can_tick = True
                if not hasattr(self, 'default_keybinds'): # Ignore if `default_keybinds` is set
                    if self.settings.has_keybinds: self.keybinds = more_args.get('keybinds', self.settings.default_keybinds)
                self.infos.has_keybinds = self.settings.has_keybinds
            self.infos.can_tick = self.can_tick

            # Format & Looks
            #if self.settings.has_optional_colour: self.has_colour = more_args.get('has_colour', True)
            self.colour = curses.color_pair(1)
            if self.settings.has_text: self.text = more_args.get('text', '')
            #if self.settings.has_formatting: pass
        else:
            log(LogLevel.WARNING, f'{widget_type}: ({self.widget_id}) No settings found! Using Defaults..')

            # Defaults
            self.infos.has_components = False
            self.components = []

            self.infos.has_multiple_components = False
            self.can_scroll = False
            self.infos.can_scroll = self.can_scroll

            self.infos.has_selected_components = False
            self.show_selected = False
            self.selected = 0

            self.wanted_width = 1
            self.wanted_height = 1

            self.can_tick = False
            self.keybinds = KeybindList()

        ## Window ##
        if not (window is None):
            self.set_window(window)
        else:
            self.window = None


        ## Keybinds ##
        self.keybind_translator = {}


        ## Custom Init ##
        if hasattr(self, 'extra_init'):
            try:
                self.extra_init(more_args)
            except Exception as e:
                log(LogLevel.ERROR, f"{self.widget_id}: Could not run extra init: {e}")

    #-#-#-# NEEDED FUNCTIONS #-#-#-#
    def set_window(self, window) -> None:
        if window is None: return

        if hasattr(self, 'set_window_self'):
            self.set_window_self(window)
        else:
            if window == "default": self.window = SHARED_VARS["STDSCR"]
            else:                   self.window = window

            if self.infos.has_components:
                self.component_pad = curses.newpad(100, 200)
                #self.component_pad.border(0)

        if self.infos.has_components:
            if hasattr(self, 'set_window_components'):
                self.set_window_components(window)
            else:
                for component, function in self.components:
                    component.set_window(self.component_pad)
        
        self.resize(new_width=self.window.getmaxyx()[1], new_height=self.window.getmaxyx()[0])

    def resize(self, new_width: int=None, new_height: int=None) -> None:
        if new_width is None: new_width = self.window.getmaxyx()[1]
        if new_height is None: new_height = self.window.getmaxyx()[0]

        # resize_self
        if hasattr(self, 'resize_self'):
            self.resize_self(new_width, new_height)
        else:
            self.width = new_width
            self.height = new_height

            if self.settings.has_components:
                if self.width > self.component_pad.getmaxyx()[1]:
                    self.component_pad.resize(self.component_pad.getmaxyx()[0], self.width)
                if self.height > self.component_pad.getmaxyx()[0]:
                    self.component_pad.resize(self.height, self.component_pad.getmaxyx()[1])

        # resize_components
        if self.settings.has_components:
            if hasattr(self, 'resize_components'):
                self.resize_components(new_width, new_height)
            else:
                for component, function in self.components:
                    component.resize(new_width, new_height)

    def tick(self, keypress:int, pass_tick_on:bool=True) -> List[Tuple[WidgetTickResult, FunctionTickResult]]:
        """ Return values:
                List(
                    Tuple(
                        WidgetTickResult,
                        FunctionTickResult
                    ),
                    ...
                )
        """

        # Init Results
        results = []
        if self.infos.has_multiple_components: results.append((WidgetTickResult(self.widget_id, keypress, self.selected), FunctionTickResult()))
        else:                                  results.append((WidgetTickResult(self.widget_id, keypress),                FunctionTickResult()))

        # Error handeling
        if not self.can_tick:
            #raise BoxesTUI_LibraryUsageError(f'{widget_type}: This Widget can not tick!')
            log(LogLevel.WARNING, f'{self.widget_type}: This Widget can not tick!')
            return results
        
        if (keypress is None) or (keypress == -1):
            return results

        # tick_self
        if self.infos.has_keybinds:
            log(LogLevel.DEBUG, f"{self.widget_id}: Ticking self; keypress: {keypress}")
            if hasattr(self, 'tick_self'):
                results[-1][1] = self.tick_self(keypress)
            else:
                for x in self.keybinds.keybinds.keys():
                    try:
                        if (isinstance(x, int) and (keypress == x)) or (isinstance(x, tuple) and (keypress in x)):

                            if self.keybinds.keybinds[x][0] in self.keybind_translator.keys():

                                if isinstance(self.keybind_translator[self.keybinds.keybinds[x][0]], tuple) and callable(self.keybind_translator[self.keybinds.keybinds[x][0]][0]):
                                    result_function, *arguments = self.keybind_translator[self.keybinds.keybinds[x][0]]
                                    results[-1] = (results[0], result_function(*arguments))
                                else:
                                    results[-1] = (results[0], self.keybind_translator[self.keybinds.keybinds[x][0]]())

                            elif callable(self.keybinds.keybinds[x][0]):
                                try:
                                    results[-1] = (results[0], self.keybinds.keybinds[x][0]())
                                except Exception as e:
                                    log(LogLevel.WARNING, f'{self.widget_type}: ({self.widget_id}) Could not Call "{self.keybinds.keybinds[x][0]}": {e}')

                            elif isinstance(self.keybinds.keybinds[x][0], tuple) and callable(self.keybinds.keybinds[x][0][0]):
                                try:
                                    result_function, *arguments = self.keybinds.keybinds[x][0]
                                    results[-1] = (results[0], result_function(*arguments))
                                except Exception as e:
                                    log(LogLevel.WARNING, f'{self.widget_type}: ({self.widget_id}) Could not Call "{self.keybinds.keybinds[x][0][0]}": {e}')

                            return results
                    except Exception as e:
                        log(LogLevel.WARNING, f'{self.widget_type}: ({self.widget_id}) Could not Process keypress "{keypress}": {e}')

        # tick_components
        if pass_tick_on and self.infos.has_components:
            if hasattr(self, 'tick_components'):
                results += self.tick_components(keypress)
            else:
                log(LogLevel.DEBUG, f"{self.widget_id}: Ticking {self.components[self.selected][0].widget_id}")
                results += self.components[self.selected][0].tick(keypress)

        return results

    def render_self(self, x:int=0, y:int=0, is_selected:bool=False) -> None:
        log(LogLevel.WARNING, f'{self.widget_type}: ({self.widget_id}) No custom render_self function defined but called.')
        if self.window is None:
            raise BoxesTUI_LibraryUsageError(f'({widget_type}: id: {self.id}) self.window is not set; did you forget to pass in a window?')

    def render_components(self, x:int=0, y:int=0) -> None:
        log(LogLevel.WARNING, f'{self.widget_type}: ({self.widget_id}) No custom render_components function defined but called.')
        if self.window is None:
            raise BoxesTUI_LibraryUsageError(f'({widget_type}: id: {self.id}) self.window is not set; did you forget to pass in a window?')

    def render(self, x:int=0, y:int=0, is_selected:bool=False) -> None:
        """ This function bundles `render_self` and `render_components`. It should only be called by the global scope, not by a widget! """

        self.render_self(x=x, y=y, is_selected=is_selected)

        if self.window.is_wintouched():
            try:
                self.window.noutrefresh()
            except Exception as e:
                log(LogLevel.ERROR, f'{self.widget_type}: ({self.widget_id}) Could not refresh the window (was maybe the `render` function called without giving the widget `STDSCR`?): {e}.')

        if self.infos.has_components:
            self.render_components(x=x, y=y)

        curses.doupdate()


    #-#-#-# MISC #-#-#-#

    def change_text(self, new_text:str) -> None:
        self.text = new_text

    def root(self) -> None:
        if "root" in SHARED_VARS["WIDGETS"].keys():
            raise BoxesTUI_LibraryUsageError(f'[{self.widget_type}]: ID "root" defined twice!')
        SHARED_VARS["WIDGETS"]["root"] = self
