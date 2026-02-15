# ###############
# ### Wrapper ###
# ###############

#  - `tui_wrapper`: the wrapper for TUI apps
#  - `quit_app`: the cleanup function for TUI apps



# ###############
# ### Imports ###
# ###############

import curses

from boxes_tui.shared_vars import SHARED_VARS
from boxes_tui.looks import ColourScheme, DEFAULT_COLOURS, init_colours
from boxes_tui.logger import *


# ###############
# ### Wrapper ###
# ###############

def tui_wrapper(function, colour_scheme: ColourScheme = DEFAULT_COLOURS, non_blocking_getch: bool = True) -> None:
    """This function calls the given function using the curses wrapper and sets some global variables"""

    def runner(stdscr) -> None:
        """This function gets called using the curses wrapper and sets some variables before calling the given function"""

        ## SHARED_VARS
        SHARED_VARS["STDSCR"] = stdscr
        set_log_file("boxes_tui.log")
        SHARED_VARS["NON_BLOCKING_GETCH"] = non_blocking_getch

        ## Curses settings
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        SHARED_VARS["STDSCR"].keypad(True)

        ## Colours
        init_colours(colour_scheme)

        try:
            function()
        except KeyboardInterrupt:
            quit_app()

    curses.wrapper(runner)


# ############
# ### Quit ###
# ############

def quit_app() -> None:
    curses.nocbreak()
    SHARED_VARS["STDSCR"].keypad(False)
    curses.echo()
    quit()
