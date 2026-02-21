# ###############
# ### Widgets ###
# ###############

# Widgets are the main components of a TUI layout made with boxes.  
# Using them you can make whatever you desire! (hopefully)

# Option include:

#  - Labels: don't have 
#  - Boxes: just a simple box containing exactly one child
#  - Layouts: some more advanced layout options; Vertical/Horizontal Layouts, which are just a "listing" of their children
#  - **TODO**: finish / extend list


# Visual example:

# ```
# +screen/term window---------------------------------------------------------+
# | +VerticalLayout---------------------------------------------------------+ |
# | | ┌───────────────────────────────────────────────────────────────────┐ | |
# | | │ This is a label in a Box, in a VerticalLayout, in a TUI!          │ | |
# | | │                                                                   │ | |
# | | └───────────────────────────────────────────────────────────────────┘ | |
# | | ╔═══════════════════════════════════════════════════════════════════╗ | |
# | | ║ +VerticalLayout-------------------------------------------------+ ║ | |
# | | ║ |  This box looks diffrent!                                     | ║ | |
# | | ║ |  Execute some function!                                       | ║ | |
# | | ║ | >This option is selected!<                                    | ║ | |
# | | ║ |  Quit                                                         | ║ | |
# | | ║ |                                                               | ║ | |
# | | ║ +---------------------------------------------------------------+ ║ | |
# | | ╚═══════════════════════════════════════════════════════════════════╝ | |
# | | You can put a label here too!                                         | |
# | +-----------------------------------------------------------------------+ |
# +---------------------------------------------------------------------------+
# ```


# **Note**: the `+-------+` boxes don't render and are here to visualise the layout better. Without it would look something like this:

# ```
# ┌─────────────────────────────────────────────────────────────────┐
# │ This is a label in a Box, in a VerticalLayout, in a TUI!        │
# │                                                                 │
# └─────────────────────────────────────────────────────────────────┘
# ╔═════════════════════════════════════════════════════════════════╗
# ║  This box looks diffrent!                                       ║
# ║  Execute some function!                                         ║
# ║ >This option is selected!<                                      ║
# ║  Quit                                                           ║
# ║                                                                 ║
# ╚═════════════════════════════════════════════════════════════════╝
# You can put a label here too!
# ```
 
# **Note**: all of this is just a rough mock-up, as I can't really draw this here as *close-to-natura* as I would like. I'll maybe add pictures to this. If I don't forget...



# ###############
# ### Exports ###
# ###############

# The main widget class:
from boxes_tui.widgets.widget import Widget

# Some pre-build widgets: (at least all that are done)
from boxes_tui.widgets.basic import Label, Textbox
from boxes_tui.widgets.boxes import Box
from boxes_tui.widgets.layouts import VerticalLayout, HorizontalLayout, Pages
from boxes_tui.widgets.global_widget import Global
