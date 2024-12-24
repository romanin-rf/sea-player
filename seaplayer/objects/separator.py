from textual.widgets import Static
from rich.console import RenderableType
from textual.visual import SupportsVisual
# ! Typing
from typing_extensions import Union

# ! Horizontal Separator Widget Class

class HorizontalSeporator(Static):
    DEFAULT_CSS = """
    HorizontalSeporator {
        height: 1;
        width: 1fr;
    }
    """

# ! Vertical Separator Widget Class

class VerticalSeporator(Static):
    DEFAULT_CSS = """
    VerticalSeporator {
        height: 1fr;
        width: 1;
    }
    """