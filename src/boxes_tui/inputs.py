# ##############
# ### Inputs ###
# ##############

#  - `KeybindList`: A list / manager for keybinds
#  - `KEY`: A map of a bunch of often-used keys
#  - **Defaults**:
#      - `STANDARD_KEYBINDS_GLOBAL`: The standard keybindings for the global TUI
#      - `STANDARD_KEYBINDS_MENU`: The standard keybindings for the menus

# ### Imports ###

import curses
import asyncio
from enum import IntEnum

from boxes_tui.wrapper import quit_app


# ### Main class ###

class KeybindList:
    """ This class just holds a bunch of keybinds for menus or the global tui.

        Keybind structure:

        tuple(
            tuple(
                key1: int,
                key2: int,
                ...
            ),
            function_to_call: function,
            description: str (optional)
        )
    """

    def __init__(self, *keybinds: tuple) -> None:
        """Arguments:
            tuple(tuple(key1: int, key2: int, ...),
                  function_to_call: function,
                  description: str (optional)
            )
        """

        self.keybinds = {}

        for keybind in keybinds:
            if len(keybind) < 2 or len(keybind) > 3:
                raise ValueError('Keybind must be: tuple(tuple(key1, key2, ...), function, description)')
            keys, function_to_call = keybind[:2]
            description = keybind[2] if len(keybind) == 3 else None
            self.keybinds[keys] = (function_to_call, description)


# ### Keymap ###

class Key(IntEnum): # TODO: Expand this list futher
    ## Arrowkeys
    up =        curses.KEY_UP
    down =      curses.KEY_DOWN
    left =      curses.KEY_LEFT
    right =     curses.KEY_RIGHT
    ## Extra Keys
    back =      curses.KEY_BACKSPACE
    enter =     curses.KEY_ENTER
    home =      curses.KEY_HOME
    end =       curses.KEY_END
    page_up =   curses.KEY_PPAGE
    page_down = curses.KEY_NPAGE
    ## F1-12
    F1 =        curses.KEY_F1
    F2 =        curses.KEY_F2
    F3 =        curses.KEY_F1
    F4 =        curses.KEY_F4
    F5 =        curses.KEY_F5
    F6 =        curses.KEY_F6
    F7 =        curses.KEY_F7
    F8 =        curses.KEY_F8
    F9 =        curses.KEY_F9
    F10 =       curses.KEY_F10
    F11 =       curses.KEY_F11
    F12 =       curses.KEY_F12


# ### Defaults

DEFAULT_KEYBINDS_GLOBAL = KeybindList(
    ((ord('q'), ord('Q')), quit_app, "Quit the TUI application"),
)

DEFAULT_KEYBINDS_MENU = KeybindList( # TODO: Add descriptions
    ((Key.up),          "menu_function_up"),
    ((Key.down),        "menu_function_down"),
    ((Key.enter, 10),   "menu_function_select"),
    ((Key.back),        "menu_function_back")
)

