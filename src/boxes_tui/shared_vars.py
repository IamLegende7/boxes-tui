# ########################
# ### Global Variables ###
# ######################## 

# - `STDSCR`: equal to the `stdscr` given by the curses wrapper - just global
# - `COLOURS`: a tranlator for curses colour pairs. **Note**: Not all pairs might be given here!

SHARED_VARS = {
    "STDSCR": None,
    "COLOURS": {"white-black": 0},
    "LOG_FILE": None,
    "LOG_LEVEL": 2, # the minimum Log_Level to log
    "WIDGETS": {},
    "NON_BLOCKING_GETCH": True  # if Global widget's .getch() should be blocking or not: blocking -> less resources take up, waits for user input ; non-blocking -> checks for term resizes, program can do something while no inputs
}

def find_widget(widget_id:str):
    """Finds a Widget by it's ID"""

    if widget_id == "STDSCR":
        return SHARED_VARS["STDSCR"]
    else:
        return SHARED_VARS["WIDGETS"][widget_id]

