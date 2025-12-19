from boxes_tui import wrapper, quit_app
from boxes_tui.shared_vars import SHARED_VARS
from boxes_tui.widgets import Label, VerticalLayout, Box
from boxes_tui.logger import LogLevel, log
from boxes_tui.inputs import KeybindList

def my_function():
    """ Use this to get the named colours currently initialised """
    log(LogLevel.DEBUG, f'{SHARED_VARS["COLOURS"]}')

def main():
    status_label = Label(
        text="HI!",
        widget_id="status_label"
    )
    status_box = Box(
        component = status_label,
        widget_id="header_box",
        wanted_height = 3
    )
    my_menu = VerticalLayout(
        components = [
            (Label(
                text="//§ C:green, bold §//Hello World!",
                widget_id="hello_world_label"
            ), my_function),
            (Label(
                text="//§ C:blue, italic, //S C:blue-reverse, italic S// §//Foo //§ C:yellow, underline, //S C:yellow-reverse, underline S// §//Bar",
                widget_id="foo_label"
            ), None),
            (Label(
                text="//§ C:red, bold, //S C:red-reverse, bold S// §//Quit",
                widget_id="quit_label"
            ), quit_app)
        ],
        widget_id="my_menu"
    )
    my_box = Box(
        component = my_menu,
        widget_id="my_box"
        #,window = "default"
    )
    big_menu = VerticalLayout(
        components = [status_box, my_box],
        widget_id="big_menu",
        window = "default",
        keybinds = KeybindList(
            ((ord("W"), ord("w")), "menu_function_up",   "Selects the last component of the Menu."),
            ((ord("S"), ord("s")), "menu_function_down", "Selects the next component of the Menu.")
        ),
        selected=1
    )

    while True:
        big_menu.render()
        #my_box.render()
        keypress = SHARED_VARS["STDSCR"].getch()
        status_label.change_text(str(keypress))
        big_menu.tick(keypress)
        #my_box.tick(keypress)

if __name__ == "__main__":
    wrapper(main)