from boxes_tui import wrapper, quit_app, find_widget
from boxes_tui.widgets import Global, VerticalLayout, Pages, Label, Box
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
    todo_tui = Global(
        widget_id = "my_tui",
        component = VerticalLayout(
            components = [
                Box(
                    widget_id="header_box",
                    component=Label(text=str("//§C:green,bold§//boxes-tui//§bold§//  --  //§C:blue,bold§//TODO" + " " * (SHARED_VARS["STDSCR"].getmaxyx()[1]-2 - len("boxes_tui  --  TODO") - len(TODOS[0].date) -1) + TODOS[0].date), widget_id="header_label"),
                    wanted_height=3
                ),
                Box(
                    widget_id="main_box",
                    component=Pages(
                        components = [VerticalLayout(widget_id="select_menu")],
                        widget_id="pages"
                    )
                )
            ],
            keybinds=KeybindList(
                ((Key.back), (find_widget("pages").page_switch, 0))
            ),
            selected = 1,
            window = "default",
            widget_id="main_layout"
        )
    )

    i = 1
    for todo in TODOS:
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
                keybinds=KeybindList(),
                show_selected=False,
                components = [
                    Label(
                        widget_id=f"todo_name_label-{todo.todo_id}",
                        text=f"//§C:green,bold§//{todo.name}"
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
        find_widget("header_label").change_text(str("//§C:green,bold§//boxes-tui//§bold§//  --  //§C:blue,bold§//TODO" + " " * (todo_tui.window.getmaxyx()[1]-2 - len("boxes_tui  --  TODO") - len(TODOS[find_widget("select_menu").selected].date) -1) + TODOS[find_widget("select_menu").selected].date))
        todo_tui.run()

if __name__ == "__main__":
    wrapper(main)