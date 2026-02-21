# #############
# ### Boxes ###
# #############


# ### IMPORTS ###

import curses
from math import floor

from boxes_tui.widgets.widget import WidgetSetting, Widget

from boxes_tui.inputs import KeybindList
from boxes_tui.looks import FormattedText, format_text
from boxes_tui.logger import LogLevel, log
from boxes_tui.exceptions import *

# ### MAIN CLASS ###

class Box(Widget):
    # TODO: update vv
    """A class that draws a border arround it's components
       Arguments:
            [component]:Wiget: the widget inside the box
            [window]:curses.window = SHARED_VARS["STDSCR"]: the window of this Box, can be shared with other Widgets
            [colour]:str = '1': the colour of the box(es outline) as a string
            [widget_id]:str = None: the ID of this Box. For identification. Should be unique.
            [width]:int = -1: The (max) width of the Box. If -1: window width will be used. ALWAYS BE ON THE HIGH SIDE IF YOU DON'T KNOW WHICH COMPONENTS YOU WANT!
            [height]:int = -1: The (max) height of the Box. If -1: window height will be used.
            [selected]:int = 0: The component that is initially selected
            [x,y]:int = 0: The offset of the top-left corner from the passed-in-window's top-left corner
    """

    widget_type = 'Box'

    settings = WidgetSetting(
        has_components=True,
        has_multiple_components=False,
        can_scroll=False,
        has_optional_scroll=False,
        has_selected_components=True,

        default_wanted_width=-1,
        default_wanted_height=-1,

        can_tick=True,
        has_optional_ticking=False,
        has_keybinds=False,

        has_optional_colour=True,
        has_text=True,
        default_show_selected=False,
        has_formatting=True
    )

    def resize_self(self, new_width:int, new_height:int) -> None:
        self.width = new_width
        self.height = new_height

        if self.width > self.component_pad.getmaxyx()[1]:
            self.component_pad.resize(self.component_pad.getmaxyx()[0], self.width)
        if self.height > self.component_pad.getmaxyx()[0]:
            self.component_pad.resize(self.height, self.component_pad.getmaxyx()[1])

    def resize_components(self, new_width:int, new_height:int) -> None: # TODO: implement scroll
        # Width
        if (self.components[0][0].wanted_width is None) or (self.components[0][0].wanted_width < 0):
            component_width = floor(self.width-2 / (-self.components[0][0].wanted_width))
        else:
            component_width = self.components[0][0].wanted_width
        # Height
        if (self.components[0][0].wanted_height is None) or (self.components[0][0].wanted_height < 0):
            component_height = floor(self.height-2 / (-self.components[0][0].wanted_height))
        else:
            component_height = self.components[0][0].wanted_height

        # Pass on
        #log(LogLevel.DEBUG, f'{self.widget_type}: Resizing component: {component_height} {component_width}')
        self.components[0][0].resize(new_width=component_width, new_height=component_height)

    # Ticking is done in the default functions in the Widget Class!

    def render_self(self, x:int=0, y:int=0, is_selected:bool=False) -> None:
        """Renders the Box of the `Box` widget"""

        if is_selected:
            tl_chr = '╔' # TODO: make variable!
            bl_chr = '╚'
            tr_chr = '╗'
            br_chr = '╝'
            sd_chr = '║'
            tp_chr = '═'
        else:
            tl_chr = '┌'
            bl_chr = '└'
            tr_chr = '┐'
            br_chr = '┘'
            sd_chr = '│'
            tp_chr = '─'

        if self.window is None:
            raise BoxesTUI_LibraryUsageError(f'({self.widget_type}: id: {self.widget_id}) self.window is not set; did you forget to pass in a window?')

        ## Render Box ##
        if True: # TODO: implement old_render_options again
        #if ((self.old_render_options.x != x) or (self.old_render_options.y != y) or (self.old_render_options.is_selected != is_selected)):
            #self.old_render_options = WidgetRenderOptions(x+self.x_offset, y+self.y_offset, is_selected)
            
            # Top
            try: self.window.addstr(y, x, tl_chr + tp_chr * (self.width-2) + tr_chr, self.colour) # TODO: add extra options, like bold, italic and stuff
            except: pass
            # Sides
            for i in range(1, self.height-2+1):
                # Left
                try: self.window.addstr(y+i, x, sd_chr, self.colour)
                except: pass
                # Right
                try: self.window.addstr(y+i, x+self.width-1, sd_chr, self.colour)
                except: pass

            # Bottom
            try: self.window.addstr(y+self.height-1, x, bl_chr + tp_chr * (self.width-2) + br_chr, self.colour)
            except: pass

    def render_components(self, x:int=0, y:int=0) -> None:
        """Renders the Components of the `Box` Widget"""

        if len(self.components) == 0:
            return

        self.components[0][0].render_self(x=0, y=0, is_selected=self.show_selected)

        if self.component_pad.is_wintouched():
            try:
                self.component_pad.noutrefresh(0,0,  y+1,x+1, self.height-2+y,self.width-2+x)
            except curses.error as e:
                log(LogLevel.ERROR, f'{self.widget_id}: Refreshing Componentpad Failed: 0,0,  {y+1},{x+1},  {self.height-2+y},{self.width-2+y}: {e}')
        
        self.components[0][0].render_components(x=x+1, y=y+1)