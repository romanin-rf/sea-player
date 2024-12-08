from textual.widgets import Static
# > Typing
from typing import Literal

# ! Nofys Classes
class Nofy(Static):
    DEFAULT_CSS = """
    Nofy {
        layer: nofys;
        background: $background;
        margin: 2 4;
        padding: 1 2;
        width: auto;
        height: auto;
    }
    """
    
    def __init__(
        self,
        text: str,
        life_time: float=3,
        dosk: Literal["bottom", "left", "right", "top"]="top",
        **kwargs
    ) -> None:
        super().__init__(text, **kwargs)
        self.life_time = life_time
        self.styles.dock = dosk
    
    def on_mount(self) -> None:
        self.set_timer(self.life_time, self.remove)
    
    async def on_click(self) -> None:
        await self.remove()

# ! Variant Nofy
class CallNofy(Static):
    DEFAULT_CSS = """
    CallNofy {
        layer: nofys;
        background: $background;
        margin: 2 4;
        padding: 1 2;
        width: auto;
        height: auto;
    }
    """
    
    def __init__(
        self,
        text: str,
        dosk: Literal["bottom", "left", "right", "top"]="top",
        **kwargs
    ) -> None:
        super().__init__(text, **kwargs)
        self.styles.dock = dosk