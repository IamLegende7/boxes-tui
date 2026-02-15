# #############
# ### Label ###
# #############


# ### IMPORTS ###

from boxes_tui.widgets.widget import WidgetSetting, Widget, WidgetTickResult, FunctionTickResult

from boxes_tui.inputs import KeybindList, DEFAULT_KEYBINDS_MENU
from boxes_tui.looks import FormattedText, format_text
from boxes_tui.logger import LogLevel, log

from boxes_tui.shared_vars import SHARED_VARS, find_widget


# ### MAIN CLASS ###

class Label(Widget):
    widget_type = "Label"

    settings = WidgetSetting(
        has_components=False,
        has_multiple_components=False,
        can_scroll=False,
        has_optional_scroll=False,
        has_selected_components=False,

        default_wanted_width=1,
        default_wanted_height=1,

        can_tick=False,
        has_optional_ticking=False,
        has_keybinds=False,

        has_optional_colour=True,
        has_text=True,
        default_show_selected=False,
        has_formatting=True
    )

    def extra_init(self, more_args):
        # Set the wanted width according to the Text len
        actual_text = ""
        for text_piece in format_text(self.text):
            actual_text += text_piece.text
        self.wanted_width = len(actual_text)

    def tick(self, keypress:int, pass_tick_on:bool=True):
        # define `tick` to prevent a warning message from being logged
        return (WidgetTickResult(self.widget_id, keypress), FunctionTickResult())

    def render_self(self, x:int=0, y:int=0, is_selected:bool=False) -> None:
        formatted_text = format_text(self.text, selected=is_selected)

        x_full = x
        for text_piece in formatted_text:
            try:
                self.window.addnstr(y, x_full, text_piece.text, self.width, text_piece.colour_pair | text_piece.additional_options)
                x_full += len(text_piece.text)
            except Exception as e:
                log(LogLevel.ERROR, f'{self.widget_type}: Could not render at {x}|{y}: {e}')
    
    def render_components(self, x:int=0, y:int=0, is_selected:bool=False) -> None:
        # define `render_components` to prevent a warning message from being logged
        pass

    def change_text(self, new_text:str) -> None:
        if new_text == self.text:
            return

        old_text = self.text
        super().change_text(new_text)
        actual_text = ""
        for text_piece in format_text(self.text):
            actual_text += text_piece.text
        self.wanted_width = len(actual_text)

        if len(self.text) != len(old_text):
            find_widget("root").resize()


class Textbox(Widget):
    widget_type = "Textbox"

    settings = WidgetSetting(
        has_components=False,
        has_multiple_components=False,
        can_scroll=True,
        has_optional_scroll=True,
        has_selected_components=False,

        default_wanted_width=0,
        default_wanted_height=0,

        can_tick=True,
        has_optional_ticking=True,
        has_keybinds=True,
        default_keybinds=KeybindList(),

        has_optional_colour=True,
        has_text=True,
        default_show_selected=False,
        has_formatting=True
    )

    def extra_init(self, more_args):
        # Set the wanted width and height
        self.text_lines = []
        self.text_lines += self.text.split('\n')

        # TODO: vertical scroll
        lenghts = []
        for line in self.text_lines:
            actual_text = ""
            for text_piece in format_text(self.text):
                actual_text += text_piece.text
            lenghts.append(len(actual_text))
        self.wanted_width = max(lenghts)

        # TODO finish horizontal scroll
        if self.wanted_height == 0:
            self.wanted_height = len(self.text_lines)
        elif self.wanted_height > 0:
            self.wanted_height = min(self.wanted_height, len(self.text_lines))

    def tick(self, keypress:int, pass_tick_on:bool=True):
        # define `tick` to prevent a warning message from being logged
        # TODO: optional navigation using arrow keys
        return (WidgetTickResult(self.widget_id, keypress), FunctionTickResult())

    def render_self(self, x:int=0, y:int=0, is_selected:bool=False) -> None:
        line_y = y
        for line in self.text_lines:
            formatted_text = format_text(line, selected=is_selected)

            x_full = x
            for text_piece in formatted_text:
                try:
                    self.window.addnstr(line_y, x_full, text_piece.text, self.width, text_piece.colour_pair | text_piece.additional_options)
                    x_full += len(text_piece.text)
                except Exception as e:
                    log(LogLevel.ERROR, f'{self.widget_type}: Could not render at {x}|{y}: {e}')
            line_y += 1
    
    def render_components(self, x:int=0, y:int=0, is_selected:bool=False) -> None:
        # define `render_components` to prevent a warning message from being logged
        pass

    def change_text(self, new_text:str) -> None:
        if new_text == self.text:
            return

        old_text = self.text
        super().change_text(new_text)
        actual_text = ""
        for text_piece in format_text(self.text):
            actual_text += text_piece.text
        self.wanted_width = len(actual_text)

        if len(self.text) != len(old_text):
            find_widget("root").resize()