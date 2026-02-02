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
        default_show_selected=True,
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
        # TODO: error handling: terminal space might not be enough to display everything
        # get infos
        wanted_heights = []
        variable_heights_count = 0
        variable_heights_sum = 0
        unassinged_height = self.height
        for component, function in self.components:
            wanted_height = component.wanted_height
            if wanted_height is None:
                wanted_height = -1

            wanted_heights.append(wanted_height)
            if wanted_height < 0:
                variable_heights_count += 1
                variable_heights_sum += 1/-wanted_height
            else:
                unassinged_height -= wanted_height

        # squishing
        if (variable_heights_sum >= 1) and (not self.can_scroll):
            for height_index in range(len(wanted_heights)):
                if wanted_heights[height_index] < 0:
                    wanted_heights[height_index] = -(1/-wanted_heights[height_index]) // variable_heights_count

        # applying
        log(LogLevel.DEBUG, f'{self.widget_id}: Componentpad is {self.component_pad.getmaxyx()[1]} x {self.component_pad.getmaxyx()[0]}. Size is {self.width} x {self.height}')
        for height_index in range(len(wanted_heights)):
            # width
            if (self.components[height_index][0].wanted_width is None) or (self.components[height_index][0].wanted_width == -1):
                component_new_width = floor(self.width)
            else:
                component_new_width = floor(self.components[height_index][0].wanted_width)
            
            if wanted_heights[height_index] < 0:
                component_new_height = floor(unassinged_height//-wanted_heights[height_index])
            else:
                component_new_height = floor(wanted_heights[height_index])

            log(LogLevel.DEBUG, f'Resizing {self.components[height_index][0].widget_id} to {component_new_width} x {component_new_height}')
            self.components[height_index][0].resize(new_width=component_new_width, new_height=component_new_height)

        self.update_scroll()

    # Ticking is done using the default functions of the Widget Class!

    def render_self(self, x:int=0, y:int=0, is_selected:bool=False) -> None:
        # define `render_self` to prevent a warning message from being logged
        pass

    def render_components(self, x:int=0, y:int=0) -> None:
        """Renders the Components of the `VerticalLayout` Widget"""

        full_y = 0
        i = 0
        for component, function in self.components:
            component.render_self(x=0, y=full_y, is_selected=((i == self.selected) and self.show_selected))
            full_y += component.height
            i += 1

        if self.component_pad.is_wintouched():
            #log(LogLevel.DEBUG, f'{self.widget_type}: Refreshing Componentpad: 0,0,  {y},{x},  {self.height-y},{self.width-x}')
            try:
                self.component_pad.noutrefresh(self.scroll,0,  y,x, self.height-1+y,self.width-1+x)
            except curses.error as e:
                log(LogLevel.ERROR, f'{self.widget_id}: Refreshing Componentpad Failed: {self.scroll},0,  {y},{x},  {self.height-1+y},{self.width-1+y}: {e}')

        full_y = y
        i = 0
        for component, function in self.components:
            if component.infos.has_components:
                component.render_components(x=x, y=full_y)
            full_y += component.height
            i += 1


    ### Extra Functions ###
    def add_component(self, new_component) -> None:
        if isinstance(new_component, tuple):
            self.components.append(new_component)
        else:
            self.components.append((new_component, None))

        if not (self.window is None):
            for component, function in self.components:
                component.set_window(self.component_pad)
        self.count_components += 1
        if not (self.window is None):
            self.resize_components(new_width=self.window.getmaxyx()[1], new_height=self.window.getmaxyx()[0])

    def update_scroll(self):
        if self.can_scroll and self.count_components > 0:
            prev_y = -self.scroll
            for component, function in self.components[:self.selected]: prev_y += component.height

            if   prev_y+self.components[self.selected][0].height <= 0:
                self.scroll -= self.components[self.selected][0].height
            elif prev_y+self.components[self.selected][0].height > self.height:
                self.scroll += prev_y+self.components[self.selected][0].height - self.height


    ### Keybind Functions ###
    def menu_up(self) -> None:
        if self.selected > 0:
            self.selected -= 1
            self.update_scroll()

    def menu_down(self) -> None:
        if self.selected < self.count_components - 1:
            self.selected += 1
            self.update_scroll()

    def menu_select(self):
        if (not (self.components[self.selected][1] is None)) and callable(self.components[self.selected][1]):
            return self.components[self.selected][1]()
        elif (not (self.components[self.selected][1] is None)) and isinstance(self.components[self.selected][1], tuple) and callable(self.components[self.selected][1][0]):
            component_function, *arguments = self.components[self.selected][1]
            return component_function(*arguments)
        else:
            return None

    def menu_back(self) -> None:
        # TODO
        pass


class Pages(Widget):
    # TODO: update vv
    """Contains miltiple components in a tab-like system
       Arguments:
            [components]:Wiget: the widgets inside the pages
            [window]:curses.window = SHARED_VARS["STDSCR"]: the window of this Box, can be shared with other Widgets
            [colour]:str = '1': the colour of the box(es outline) as a string
            [widget_id]:str = None: the ID of this Box. For identification. Should be unique.
            [width]:int = -1: The (max) width of the Box. If -1: window width will be used. ALWAYS BE ON THE HIGH SIDE IF YOU DON'T KNOW WHICH COMPONENTS YOU WANT!
            [height]:int = -1: The (max) height of the Box. If -1: window height will be used.
            [selected]:int = 0: The component that is initially selected
            [x,y]:int = 0: The offset of the top-left corner from the passed-in-window's top-left corner
    """

    widget_type = 'Page'

    settings = WidgetSetting(
        has_components=True,
        has_multiple_components=True,
        can_scroll=False,
        has_optional_scroll=False,
        has_selected_components=True,

        default_wanted_width=-1,
        default_wanted_height=-1,

        can_tick=True,
        has_optional_ticking=False,
        has_keybinds=True,
        default_keybinds=KeybindList(),

        has_optional_colour=False,
        has_text=False,
        default_show_selected=False,
        has_formatting=False
    )

    def extra_init(self):
        self.count_components = 0

        self.keybind_translator = {
            "page_switch": self.page_switch,
            "page_next":   self.page_next,
            "page_before": self.page_before,
            "page_select": self.page_select
        }

        new_components = []
        for x in self.components: new_components.append(x)
        self.components = []
        for x in new_components: self.add_component(x)

    def resize_self(self, new_width:int, new_height:int) -> None:
        self.width = new_width
        self.height = new_height

        if self.width > self.component_pad.getmaxyx()[1]:
            self.component_pad.resize(self.component_pad.getmaxyx()[0], self.width)
        if self.height > self.component_pad.getmaxyx()[0]:
            self.component_pad.resize(self.height, self.component_pad.getmaxyx()[1])

    def resize_components(self, new_width:int, new_height:int) -> None: # TODO: implement scroll
        for component_index in range(len(self.components)):
            # Width
            if (self.components[component_index][0].wanted_width is None) or (self.components[component_index][0].wanted_width < 0):
                component_width = floor(self.width / (-self.components[0][0].wanted_width))
            else:
                component_width = self.components[0][0].wanted_width
            # Height
            if (self.components[component_index][0].wanted_height is None) or (self.components[component_index][0].wanted_height < 0):
                component_height = floor(self.height / (-self.components[0][0].wanted_height))
            else:
                component_height = self.components[component_index][0].wanted_height

            # Pass on
            #log(LogLevel.DEBUG, f'{self.widget_type}: Resizing component: {component_height} {component_width}')
            self.components[component_index][0].resize(new_width=component_width, new_height=component_height)

    # Ticking is done in the default functions in the Widget Class!

    def render_self(self, x:int=0, y:int=0, is_selected:bool=False) -> None:
        # define `render_self` to prevent a warning message from being logged
        # TODO: make an optional tab display (like in a browser)
        pass

    def render_components(self, x:int=0, y:int=0) -> None:
        """Renders the Components of the `Pages` Widget"""

        self.components[self.selected][0].render_self(x=0, y=0, is_selected=self.show_selected)

        if self.component_pad.is_wintouched():
            try:
                self.component_pad.noutrefresh(0,0,  y,x, self.height+y-1,self.width+x-1)
            except curses.error as e:
                log(LogLevel.ERROR, f'{self.widget_id}: Refreshing Componentpad Failed: 0,0,  {y},{x},  {self.height+y},{self.width+y}: {e}')
        
        self.components[self.selected][0].render_components(x=x, y=y)


    ### Extra Functions ###
    def add_component(self, new_component) -> None:
        if isinstance(new_component, tuple):
            self.components.append(new_component)
        else:
            self.components.append((new_component, None))

        if not (self.window is None):
            for component, function in self.components:
                component.set_window(self.component_pad)
        self.count_components += 1
        if not (self.window is None):
            self.resize_components(new_width=self.window.getmaxyx()[1], new_height=self.window.getmaxyx()[0])


    ### Keybind Functions ###
    def page_switch(self, new_selected: int) -> None:
        if (new_selected >= 0) and (new_selected < self.count_components):
            self.selected = new_selected
            if not (self.window is None): self.component_pad.erase()
    
    def page_next(self) -> None:
        if self.selected > 0:
            self.selected -= 1
            if not (self.window is None): self.component_pad.erase()

    def page_before(self) -> None:
        if self.selected < self.count_components - 1:
            self.selected += 1
            if not (self.window is None): self.component_pad.erase()

    def page_select(self):
        if not (self.components[self.selected][1] is None) and callable(self.components[self.selected][1]):
            return self.components[self.selected][1]()
        else:
            return None