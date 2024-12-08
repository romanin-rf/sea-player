import random
from textual.widgets import Label, Button
from rich.style import Style
from rich.console import RenderableType
from rich.segment import Segments, Segment
# > Typing
from typing import Optional, Union, Callable, Awaitable
from inspect import iscoroutinefunction

# ! Fill Label Class
class FillLabel(Label):
    DEFAULT_CSS = """
    FillLabel {
        height: 1fr;
        width: 1fr;
    }
    """
    def __gen_random_color(self) -> None:
        return f"#{hex(random.randint(0,16777215))[2:]}"
    
    def __gen_segments(self) -> Segments:
        segments = []
        for i in range(self.size[0]*self.size[1]):
            s = Style.parse(self.__gen_random_color()) if self.__rainbow else self.__style
            segments.append(Segment(self.__chr, s))
        return Segments(segments)
    
    def __init__(
        self,
        char: str="-",
        style: Optional[Style]=None,
        rainbow: bool=False,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.__chr = char[:1]
        self.__rainbow = rainbow
        self.__style = style
        self.update(self.__gen_segments())
    
    async def on_resize(self) -> None:
        self.update(self.__gen_segments())

# ! Clickable Label Class
class ClickableLabel(Label, Button, can_focus=True):
    DEFAULT_CSS = """
    ClickableLabel {
        width: auto;
        min-width: 1;
        height: auto;
        min-height: 1;
        color: $text;
        text-style: bold;
        text-align: center;
        content-align: center middle;
    }
    ClickableLabel:focus {
        text-style: bold reverse;
    }
    ClickableLabel:hover {
        color: $text;
    }
    ClickableLabel.-active {
        tint: $background 30%;
    }
    """
    def __init__(
        self,
        renderable: RenderableType="",
        callback: Union[Callable[[], None], Callable[[], Awaitable[None]]]=lambda: None,
        *,
        expand: bool=False,
        shrink: bool=False,
        markup: bool=True,
        name: Optional[str]=None,
        id: Optional[str]=None,
        classes: Optional[str]=None,
        disabled: bool=False
    ) -> None:
        super().__init__(
            renderable,
            expand=expand,
            shrink=shrink,
            markup=markup,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled
        )
        self.__callback = callback
    
    @property
    def callback_awaitable(self) -> bool:
        return iscoroutinefunction(self.__callback)
    
    async def _on_click(self, event) -> None:
        await super()._on_click(event)
        if self.callback_awaitable:
            await self.__callback()
        else:
            self.__callback()
