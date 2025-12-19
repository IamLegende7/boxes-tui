# ######################
# ### VerticalLayout ###
# ######################


# ### IMPORTS ###

import curses
from math import floor

from boxes_tui.widgets.widget import WidgetSetting, Widget

from boxes_tui.inputs import KeybindList, DEFAULT_KEYBINDS_MENU
from boxes_tui.looks import FormattedText, format_text
from boxes_tui.logger import LogLevel, log

from boxes_tui.shared_vars import SHARED_VARS

# ### MAIN CLASS ###

class VerticalLayout(Widget):
    # TODO: update vv
    """A class for bundeling a bunch of widgets into a nice list. Can also be used as a navigatable Menu
       Arguments:
            [window]:curses.window = SHARED_VARS["STDSCR"]: the window of this Layout, can be shared with other Widgets
            [widget_id]:str = None: the ID of this Layout. For identification. Should be unique.
            [width]:int = -1: The (max) width of the Layout. If -1: window width will be used. ALWAYS BE ON THE HIGH SIDE IF YOU DON'T KNOW WHICH COMPONENTS YOU WANT!
            [height]:int = -1: The (max) height of the Layout. If -1: window height will be used. If you need to fit in more, try enabeling `can_scroll`
            [should_tick]:bool = True: wether ticking this Layout does something. If you just want a static layout, set this to False.
            [selected]:int = 0: The component that is initially selected
            [x,y]:int = 0: The offset of the top-left corner from the passed-in-window's top-left corner
            [keybinds]:KeybindsList = DEFAULT_KEYBINDS_MENU: The keybinds of this Layout. Use `KeybindList()` if you don't want any.
    """

    widget_type = "VerticalLayout"

    settings = WidgetSetting(
        has_components=True,
        has_multiple_components=True,
        can_scroll=True,
        has_optional_scroll=True,
        has_selected_components=True,

        default_wanted_width=-1,
        default_wanted_height=-1,

        can_tick=True,
        has_optional_ticking=True,
        has_keybinds=True,
        default_keybinds=DEFAULT_KEYBINDS_MENU,

        has_optional_colour=False,
        has_text=False,
        has_formatting=False
    )

    def extra_init(self):
        self.count_components = 0

        self.keybind_translator = {
            "menu_function_up":     self.menu_up,
            "menu_function_down":   self.menu_down,
            "menu_function_select": self.menu_select,
            "menu_function_back":   self.menu_back
        }

        new_components = []
        for x in self.components: new_components.append(x)
        self.components = []
        for x in new_components: self.add_component(x)

    def resize_components(self, new_width:int, new_height:int) -> None: # TODO: implement scroll # TODO: implement diffrent parts of the given space (like -2 = 1/2 of the avalible space) and mixing multiple diffrent ratios
        # Precounting
        variable_height_components = 0
        needed_height = 0
        for component, function in self.components:
            if (component.wanted_height is None) or (component.wanted_height == -1):
                variable_height_components += 1
            else:
                needed_height += component.wanted_height

        if needed_height + (variable_height_components * 2) > self.component_pad.getmaxyx()[0]:
            log(LogLevel.WARNING, f'Not enough terminal height for loading all components & I forgot to implement scroll')
            return

        # Changing components
        component_index = 0
        height_left = new_height - needed_height - 1
        for component, function in self.components:
            # Width
            if (component.wanted_width is None) or (component.wanted_width == -1):
                component_width = self.component_pad.getmaxyx()[1] - 1
            else:
                component_width = component.wanted_width
            # Height
            if (component.wanted_height is None) or (component.wanted_height == -1):
                component_height = floor(height_left / variable_height_components)
            else:
                component_height = component.wanted_height
            # Pass on
            component.resize(new_width=component_width, new_height=component_height)
            component_index += 1

    # Ticking is done in the default functions in the Widget Class!

    def render_self(self, x:int=0, y:int=0, is_selected:bool=False) -> None:
        # define `render_self` to prevent a warning message from being logged
        pass

    def render_components(self, x:int=0, y:int=0, is_selected:bool=False) -> None:
        """Renders the Components of the `VerticalLayout` Widget"""

        full_y = 0
        i = 0
        for component, function in self.components:
            component.render_self(x=0, y=full_y, is_selected=(i == self.selected))
            full_y += component.height
            i += 1

        if self.component_pad.is_wintouched():
            #log(LogLevel.DEBUG, f'{self.widget_type}: Refreshing Componentpad: 0,0,  {y},{x},  {self.height-y},{self.width-x}')
            self.component_pad.refresh(0,0,  y,x, self.height-2+y,self.width-2+x)

        full_y = y
        i = 0
        for component, function in self.components:
            if component.infos.has_components:
                component.render_components(x=x, y=full_y, is_selected=(i == self.selected))
            full_y += component.height
            i += 1


    ### Extra Functions ###
    def add_component(self, new_component) -> None:
        if isinstance(new_component, tuple):
            self.components.append(new_component)
        else:
            self.components.append((new_component, None))
        self.count_components += 1


    ### Keybind Functions ###
    def menu_up(self) -> None:
        if self.selected > 0:
            self.selected -= 1

    def menu_down(self) -> None:
        #log(LogLevel.DEBUG, 'Executing `menu_down`!')
        if self.selected < self.count_components - 1:
            self.selected += 1

    def menu_select(self):
        if not (self.components[self.selected][1] is None) and callable(self.components[self.selected][1]):
            return self.components[self.selected][1]()
        else:
            return None

    def menu_back(self) -> None:
        pass