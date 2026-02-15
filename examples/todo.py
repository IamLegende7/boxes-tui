from boxes_tui import wrapper, quit_app, find_widget
from boxes_tui.widgets import Global, VerticalLayout, Pages, Label, Textbox, Box
from boxes_tui.logger import *
from boxes_tui.inputs import KeybindList, Key
from boxes_tui.shared_vars import SHARED_VARS

from dataclasses import dataclass
import json
import time

set_log_level(LogLevel.INFO)

@dataclass
class Todo():
    name: str
    todo_id: str = 'TODO'
    description: str = "<No futher discription given>"
    importance: int = 0
    date: str = "xx xxx xxxx"

    def __post_init__(self):
        self.todo_id = f'TODO-[{self.name}]'

importance_colours = {
    0: "white",
    1: "green",
    2: "blue",
    3: "yellow",
    4: "red"
}

TODOS = []

def main():
    def update_todos():
        log(LogLevel.INFO, "Refreshing todos..")
        global TODOS
        TODOS.clear()
        for x in load_todos(): TODOS.append(x)
        log(LogLevel.CRITICAL, f"{TODOS}")
        add_todos()

    todo_tui = Global(
        widget_id = "my_tui",
        component = VerticalLayout(
            components = [
                Box(
                    widget_id="header_box",
                    component=Label(text=str("//§C:green,bold§//boxes-tui//§bold§//  --  //§C:blue,bold§//TODO"), widget_id="header_label"),
                    wanted_height=3
                ),
                Box(
                    widget_id="main_box",
                    component=Pages(
                        components = [VerticalLayout(
                            widget_id="select_menu",
                            keybinds=KeybindList(
                                ((Key.up),             "menu_function_up"),
                                ((Key.down),           "menu_function_down"),
                                ((Key.enter, 10),      "menu_function_select"),
                                ((ord("q"), ord("Q")), quit_app)
                            ),
                            can_scroll=True,
                            wrap_index=True
                        )],
                        widget_id="pages"
                    )
                )
            ],
            keybinds=KeybindList(),
            selected = 1,
            show_selected=False,
            window = "default",
            widget_id="main_layout"
        )
    )

    def load_todos(todo_path:str="TODO.json") -> list[Todo]:
        with open(todo_path, 'r') as file:
            json_data = json.load(file)
        todos_unsorted = [Todo(**item) for item in json_data]

        result = []
        for x in reversed(sorted(todos_unsorted, key=lambda todo: todo.importance)): result.append(x)

        return result

    def add_todos():
        for i in range(find_widget("select_menu").count_components):
            find_widget("select_menu").delete_component(0)
        for i in range(find_widget("pages").count_components-1):
            find_widget("pages").delete_component(1)

        i = 1
        for todo in TODOS:
            log(LogLevel.ERROR, f"Selected: {find_widget("select_menu").selected}; Length: {len(find_widget("select_menu").components)}; Length TODOS: {len(TODOS)}; Count: {find_widget("select_menu").count_components}")
            SHARED_VARS["STDSCR"].getch()
            log(LogLevel.CRITICAL, f"TODO {todo.name}")
            find_widget("select_menu").add_component(
                (
                    Label(
                        widget_id=f"todo_select_label-{todo.todo_id}",
                        text=f"//§C:{importance_colours[todo.importance]},bold§//{todo.name}"
                    ),
                    (find_widget("pages").page_switch, i)
                )
            )
            find_widget("pages").add_component(
                VerticalLayout(
                    widget_id=f'VerticalLayout-{todo.todo_id}',
                    keybinds=KeybindList(
                        ((Key.back), (find_widget("pages").page_switch, 0))
                    ),
                    show_selected=False,
                    components = [
                        Label(
                            widget_id=f"todo_name_label-{todo.todo_id}",
                            text=f"//§C:green,bold§//{todo.name}"
                        ),
                        Textbox( # TODO: this should be a textbox
                            widget_id=f"todo_description-{todo.todo_id}",
                            text=f"{todo.description}"
                        )
                    ]
                )
            )
            i += 1

    update_todos()
    prev_string = ""
    while True:
        if len(find_widget("select_menu").components) != 0:
            log_string = f"Selected: {find_widget("select_menu").selected}; Length: {len(find_widget("select_menu").components)}; Length TODOS: {len(TODOS)}; Count: {find_widget("select_menu").count_components}"
            if prev_string != log_string:
                log(LogLevel.CRITICAL, log_string)
                prev_string = log_string
            find_widget("header_label").change_text(str("//§C:green,bold§//boxes-tui//§bold§//  --  //§C:blue,bold§//TODO" + " " * (todo_tui.window.getmaxyx()[1]-2 - len("boxes_tui  --  TODO") - len(TODOS[find_widget("select_menu").selected].date) -1) + TODOS[find_widget("select_menu").selected].date))
        else:
            find_widget("header_label").change_text(str("//§C:green,bold§//boxes-tui//§bold§//  --  //§C:blue,bold§//TODO"))
        todo_tui.run()
        time.sleep(0.02)

if __name__ == "__main__":
    wrapper(main)