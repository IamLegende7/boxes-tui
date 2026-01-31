from boxes_tui import wrapper, quit_app
from boxes_tui.widgets import VerticalLayout, Pages, Label, Box
from boxes_tui.logger import LogLevel, log
from boxes_tui.inputs import KeybindList, Key
from boxes_tui.shared_vars import SHARED_VARS

from dataclasses import dataclass
import json


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

def load_todos(todo_path:str="TODO.json") -> list[Todo]:
    with open(todo_path, 'r') as file:
        json_data = json.load(file)
    return [Todo(**item) for item in json_data]
 
TODOS = []
for x in reversed(sorted(load_todos(), key=lambda todo: todo.importance)): TODOS.append(x)

def main():
    main_pages = Pages(
        components = [
            VerticalLayout(
                widget_id="main_select_menu"
            )
        ],
        widget_id="main_pages"
    )
    main_layout = VerticalLayout(
        components = [
            (Box(
                widget_id="header_box",
                component=Label(text=str("//§C:green,bold§//boxes-tui//§bold§//  --  //§C:blue,bold§//TODO" + " " * (SHARED_VARS["STDSCR"].getmaxyx()[1]-2 - len("boxes_tui  --  TODO") - len(TODOS[0].date) -1) + TODOS[0].date)),
                wanted_height=3
            )),
            Box(
                widget_id="main_box",
                component=main_pages
            )
        ],
        keybinds=KeybindList(
            ((Key.back), (main_pages.page_switch, 0))
        ),
        selected = 1,
        window = "default",
        widget_id="main_layout"
    )

    i = 1
    for todo in TODOS:
        main_pages.components[0][0].add_component(
            (
                Label(
                    widget_id=f"todo_select_label-{todo.todo_id}",
                    text=f"//§C:{importance_colours[todo.importance]},bold§//{todo.name}"
                ),
                (main_pages.page_switch, i)
            )
        )
        main_pages.add_component(
            VerticalLayout(
                widget_id=f'VerticalLayout-{todo.todo_id}',
                keybinds=KeybindList(),
                components = [
                    Label(
                        widget_id=f"todo_name_label-{todo.todo_id}",
                        text=f"//§ //S C:green, bold S// §//{todo.name}"
                    ),
                    Label( # TODO: this should be a textbox
                        widget_id=f"todo_description-{todo.todo_id}",
                        text=f"{todo.description}"
                    )
                ]
            )
        )
        i += 1

    while True:
        main_layout.components[0][0].components[0][0].change_text(str("//§C:green,bold§//boxes-tui//§bold§//  --  //§C:blue,bold§//TODO" + " " * (main_layout.window.getmaxyx()[1]-2 - len("boxes_tui  --  TODO") - len(TODOS[main_layout.components[1][0].components[0][0].components[0][0].selected].date) -1) + TODOS[main_layout.components[1][0].components[0][0].components[0][0].selected].date))
        main_layout.render()
        keypress = main_layout.window.getch()
        main_layout.tick(keypress)

if __name__ == "__main__":
    wrapper(main)