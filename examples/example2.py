from boxes_tui import wrapper, quit_app
from boxes_tui import find_widget as wdgt
from boxes_tui.widgets import Global, VerticalLayout, HorizontalLayout, Pages, Box, Label, Textbox
from boxes_tui.logger import log, LogLevel, set_log_level
from boxes_tui.inputs import KeybindList, Key
from time import sleep
import subprocess

import os
import sys
from dataclasses import dataclass

set_log_level(LogLevel.INFO)

@dataclass
class Game():
    name: str
    game_dir_path: str
    run_file: str
    description: str = ""

def main():
    Global(
        component=VerticalLayout(
            keybinds=KeybindList(),
            selected=1,
            show_selected=False,
            widget_id="main_layout",
            components=[
                Box(
                    widget_id="header_box",
                    wanted_height=3,
                    component=HorizontalLayout(
                        widget_id="header_layout",
                        wanted_height=1,
                        show_selected=False,
                        selected=1,
                        components=[
                            Label(
                                text="//§C:green,bold§//dosboxrun//§bold§// -- ",
                                widget_id="header_label1"
                            ),
                            Label(
                                text="//§C:blue,bold§//Hello",
                                widget_id="header_label2"
                            )
                        ]
                    )
                ),
                HorizontalLayout(
                    widget_id="horizontal_layout",
                    show_selected=False,
                    selected=0,
                    components=[
                        Box(
                            widget_id="main_box1",
                            component=VerticalLayout(
                                widget_id="select_menu",
                                can_scroll=True
                            )
                        ),
                        Box(
                            widget_id="main_box2",
                            component=Pages(
                                widget_id="game_pages"
                            )
                        )
                    ]
                )
            ]
        )
    )

    def run_game(game_run_file:str, log_file_path:str='dosgame.log') -> None:
        with open(log_file_path, 'w') as log_file:
            game_process = subprocess.Popen(
                ['bash', f'{game_run_file}'],
                stdout=log_file,
                stderr=log_file
            )

            game_process.wait()

    if len(sys.argv) > 1:
        dos_games_dir = sys.argv[1]
    else:
        dos_games_dir = os.getcwd()

    games = []
    log(LogLevel.INFO, f'Looking for games in {dos_games_dir}')
    for entry in sorted(os.listdir(dos_games_dir)):
        if os.path.isdir(os.path.join(dos_games_dir, entry)) and '.dosboxrun.sh' in os.listdir(os.path.join(dos_games_dir, entry)):
            log(LogLevel.INFO, f'   found game: {entry}')
            games.append(Game(
                name=entry,
                game_dir_path=str(os.path.join(dos_games_dir, entry)),
                run_file=str(os.path.join(dos_games_dir, entry, '.dosboxrun.sh'))
            ))

    for game in games:
        wdgt("select_menu").add_component((
            Label(text=game.name, widget_id=f'label-{game.name}'),
            (run_game, game.run_file)
        ))
        wdgt("game_pages").add_component((
            Textbox(
                text=f" Game Name:      {game.name}\n Game Directory: {game.game_dir_path}\n Execution File: {game.run_file}"
            )
        ))

    has_quit = False
    while not has_quit:
        wdgt("root").run()
        wdgt("game_pages").page_switch(wdgt("select_menu").selected)
        sleep(0.02)


if __name__ == "__main__":
    wrapper(main)