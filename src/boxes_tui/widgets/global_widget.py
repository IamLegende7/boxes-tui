# #####################
# ### Global Widget ###
# #####################


# ### IMPORTS ###

import curses
from math import floor

from boxes_tui.widgets.widget import WidgetSetting, Widget

from boxes_tui.inputs import KeybindList
from boxes_tui.looks import FormattedText, format_text
from boxes_tui.logger import LogLevel, log

from boxes_tui.shared_vars import SHARED_VARS

# ### MAIN CLASS ###

class Global(Widget):
    """ A class that automates a bunch of functions by bundeling the TUI's first widget as it's component
        Arguments:
            TODO
    """

    widget_type = 'Global'

    settings = WidgetSetting(
        has_components=True,
        has_multiple_components=False,
        can_scroll=False,
        has_optional_scroll=False,
        has_selected_components=False,

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

    def extra_init(self, more_args):
        self.root()
        self.set_window(SHARED_VARS["STDSCR"])
        self.window.nodelay(SHARED_VARS["NON_BLOCKING_GETCH"])

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

    def render_self(self, x:int=0, y:int=0, is_selected:bool=False) -> None:
        # define `render_self` to prevent a warning message from being logged
        pass

    def render_components(self, x:int=0, y:int=0) -> None:
        """Renders the Components of the `Global` Widget"""

        self.components[self.selected][0].render_self(x=0, y=0, is_selected=self.show_selected)

        if self.component_pad.is_wintouched():
            try:
                self.component_pad.noutrefresh(0,0,  y,x, self.height+y-1,self.width+x-1)
            except curses.error as e:
                log(LogLevel.ERROR, f'{self.widget_id}: Refreshing Componentpad Failed: 0,0,  {y},{x},  {self.height+y},{self.width+y}: {e}')
        
        self.components[self.selected][0].render_components(x=x, y=y)

    def run(self) -> int:
        if self.window is None:
            return None
        self.render()
        
        try:
            keypress = self.window.getch()
        except curses.error:
            keypress = None

        if keypress == curses.KEY_RESIZE:
            self.resize(self.window.getmaxyx()[1], self.window.getmaxyx()[0])

        tick_result = self.tick(keypress)

        return tick_result