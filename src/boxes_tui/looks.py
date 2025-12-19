#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import curses
from enum import Enum

from boxes_tui.shared_vars import SHARED_VARS
from boxes_tui.logger import LogLevel, log


# In[ ]:


class colour(Enum):
    default = -1
    white   = curses.COLOR_WHITE
    black   = curses.COLOR_BLACK
    red     = curses.COLOR_RED
    green   = curses.COLOR_GREEN
    blue    = curses.COLOR_BLUE
    yellow  = curses.COLOR_YELLOW
    cyan    = curses.COLOR_CYAN
    magenta = curses.COLOR_MAGENTA


# In[ ]:


class ColourScheme:
   """A simple class to hold a bunch of colour pairs to be used in `init_colours`
      Arguments:
         colour_pair1: tuple(number: int, foreground: str, background: str, name: str (optional)),
         colour_pair2,
         ...
      foreground & background colours are from `colour`, otherwise will just be interpreted as ints
   """

   def __init__(self, *colour_pairs) -> None:
      ## TODO: add error handeling!
      self.colour_pairs = colour_pairs


# In[ ]:


DEFAULT_COLOURS = ColourScheme(
    (1,  colour.white,   colour.default,   "white"),
    (2,  colour.black,   colour.default,   "black"),

    (3,  colour.red,     colour.default,   "red"),
    (4,  colour.white,   colour.red,       "red-reverse"),

    (5,  colour.green,   colour.default,   "green"),
    (6,  colour.black,   colour.green,     "green-reverse"), # Bright-on-Bright colours don't work in some terminals (VSCode, for instamce), the foreground colour will be a gray-tone

    (7,  colour.blue,    colour.default,   "blue"),
    (8,  colour.white,   colour.blue,      "blue-reverse"),

    (9,  colour.yellow,  colour.default,   "yellow"),
    (10, colour.black,   colour.yellow,    "yellow-reverse")
)


# In[ ]:


def init_colours(colours: ColourScheme = DEFAULT_COLOURS) -> None: # TODO: make coustom colours (colours not curses.SOMETHING)
    """A short function to load a ColourScheme class into curses colour pairs"""

    curses.start_color()
    curses.use_default_colors()

    for colour_pair in colours.colour_pairs:
        pair_num = colour_pair[0]
        # Foreground
        if colour_pair[1] in colour:
            foreground = colour_pair[1].value
        elif (colour_pair[1][0] in ('-', '+') and colour_pair[1][1:].isdigit()) or colour_pair[1].isdigit():
            try: foreground = int(colour_pair[1])
            except: foreground = curses.COLOR_WHITE
        else:
            foreground = curses.COLOR_WHITE # TODO: some logging here

        # Background
        if colour_pair[2] in colour:
            background = colour_pair[2].value
        elif (colour_pair[2][0] in ('-', '+') and colour_pair[2][1:].isdigit()) or colour_pair[2].isdigit():
            try: background = int(colour_pair[2])
            except: background = -1
        else:
            background = -1 # TODO: some logging here

        # Name
        if not (colour_pair[3] is None):
            SHARED_VARS["COLOURS"][colour_pair[3]] = pair_num

        ## Load
        #log(LogLevel.DEBUG, f'Setting Pair {colour_pair[3]} to {foreground} | {background}' + '\n')
        try: curses.init_pair(pair_num, foreground, background) # FIXME: Why doesn't this work?
        except Exception as e: 
            log(LogLevel.ERROR, f'Exception at: {pair_num}, {foreground} {background}: {e}' + '\n')


# ### Using Colours
# 
# ---

# In[ ]:


class FormattedText:
    def __init__(self, text: str, colour_pair: int, additional_options: int) -> None:
        self.text = text
        self.colour_pair = colour_pair
        self.additional_options = additional_options


# In[ ]:


def process_arguments(arguments: list) -> tuple:
    """This Function takes a list of option [arguments](../../README.md) and outputs it as a bunt of or'd together options"""

    ## Process ##
    colour_pair = 0
    text_options = 0

    for arg in arguments:
        #log(LogLevel.DEBUG, f'Processing Argument: {arg}' + '\n')
        if arg == '':
            continue

        # Misc
        if   arg == 'reverse':   text_options |= curses.A_REVERSE
        elif arg == 'bold':      text_options |= curses.A_BOLD
        elif arg == 'italic':    text_options |= curses.A_ITALIC
        elif arg == 'dim':       text_options |= curses.A_DIM
        elif arg == 'underline': text_options |= curses.A_UNDERLINE
        elif arg == 'standout':  text_options |= curses.A_STANDOUT
        # Colour
        elif ('C:' in arg) and (arg.split(':', 1)[0] == 'C'):
            colour_code_string = arg.split(':', 1)[1]

            if colour_code_string in SHARED_VARS["COLOURS"].keys():
                colour_pair |= curses.color_pair(SHARED_VARS["COLOURS"][colour_code_string])

            elif (colour_code_string[0] in ('-', '+') and colour_code_string[1:].isdigit()) or colour_code_string.isdigit():
                try:    colour_pair |= curses.color_pair(int(colour_code_string))
                except: colour_pair |= curses.color_pair(1)

            else:
                colour_pair |= curses.color_pair(1) 

        # Extra Arg
        else:
            try: text_options |= int(arg)
            except:
                log(LogLevel.ERROR, f'Not an int: {arg}' + '\n')

    return text_options, colour_pair


# In[ ]:


def format_text(unformatted_text: str, selected: bool = True) -> list:

    result = []

    ## Split ##
    text_parts = unformatted_text.replace('\n', '').replace('\r', '').split('//§')
    for part in text_parts:
        if part == '':
            continue

        # Arguments & text parts
        arguments_normal = []
        arguments_selected = []

        if ('§//' in part):
            text_piece = part.split('§//')[1]

            arguments = part.split('§//')[0].split(',')
            for i in range(len(arguments)): arguments[i] = arguments[i].strip()

            handeling_selected_arguments = False
            for argument in arguments:
                if '//S' in argument:
                    handeling_selected_arguments = True
                    argument = argument.split('//S', 1)[1].strip()
                if 'S//' in argument:
                    handeling_selected_arguments = False
                    arguments_selected.append(argument.split('S//', 1)[0].strip())
                    continue

                if handeling_selected_arguments: arguments_selected.append(str(argument))
                else:                            arguments_normal.append(str(argument))
        else:
            text_piece = part

        if len(arguments_selected) == 0:
            for x in arguments_normal: arguments_selected.append(x)
            arguments_selected.append(str(curses.A_REVERSE))

            #log(LogLevel.DEBUG, f'Normal: {arguments_normal}, Selected: {arguments_selected} Text: {text_piece}' + '\n')

        if selected: text_options, colour_pair = process_arguments(arguments_selected)
        else:        text_options, colour_pair = process_arguments(arguments_normal)

        result.append(FormattedText(text=text_piece, additional_options=text_options, colour_pair=colour_pair))

    return result

