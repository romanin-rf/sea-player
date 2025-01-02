from time import time
from textual.app import RenderResult
from textual.color import Color, Gradient
from textual.widgets import LoadingIndicator
# > Rich
from rich.style import Style
from rich.text import Text, TextType
# > Typing
from typing_extensions import (
    Tuple,
)


# ! Main Class

class AnimatedGradientText(LoadingIndicator):
    DEFAULT_CSS = """
    AnimatedGradientText {
        height: 1fr;
        width: 1fr;
    }
    """
    
    def __init__(self,
        text: TextType='Loading...',
        gradient_colors: Tuple[Color, Color] | None = None,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ):
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        _, _, background, color = self.colors
        
        self._text: str = str(Text(text))
        self._gradbg, self._gradclr = gradient_colors or (background, color)
        self._start_time: float = 0.0
    
    def render(self) -> RenderResult:
        if self.app.animation_level == "none":
            return Text(self._text)
        
        elapsed = time() - self._start_time
        speed = 0.8

        gradient = Gradient(
            (0.0, self._gradbg.blend(self._gradclr, 0.1)),
            (0.7, self._gradclr),
            (1.0, self._gradclr.lighten(0.1)),
        )
        
        divlen = 8 if (len(self._text) < 8) else len(self._text)

        blends = [(elapsed * speed - char_number / divlen) % 1 for char_number in range(divlen)]

        chars = [
            (
                char, Style.from_color(gradient.get_color((1 - blend) ** 2).rich_color),
            )
            for char, blend in zip(self._text, blends)
        ]
        return Text.assemble(*chars)