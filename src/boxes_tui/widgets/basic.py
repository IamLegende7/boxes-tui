# #############
# ### Label ###
# #############


# ### IMPORTS ###

from boxes_tui.widgets.widget import WidgetSetting, Widget, WidgetTickResult, FunctionTickResult

from boxes_tui.looks import FormattedText, format_text
from boxes_tui.logger import LogLevel, log


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
        has_formatting=True
    )

    def extra_init(self):
        # Set the wanted width according to the Text len
        actual_text = ""
        for text_piece in format_text(self.text):
            actual_text += text_piece.text
        self.wanted_width = len(actual_text)

    def tick(self, keypress:int, pass_tick_on:bool=True):
        # define `ticks` to prevent a warning message from being logged
        return (WidgetTickResult(self.widget_id, keypress), FunctionTickResult(None))

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