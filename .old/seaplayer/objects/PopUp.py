from textual.widget import Widget
from textual.widgets import Label
from textual.containers import Container
# > Typing
from typing import Optional
# > Local Imports
from .Labels import FillLabel

# ! Main Class
class PopUp(Container):
    DEFAULT_CSS = """
    PopUp {
        layer: popup;
        background: $background;
        text-align: center;
        align-vertical: middle;
        align-horizontal: center;
        content-align: center middle;
        width: auto;
        height: auto;
        padding: 1 2 1 2;
    }
    """
    pass

# ! Other Clases
class PopUpWindow(PopUp):
    DEFAULT_CSS = """
    PopUpWindow {
        layer: popup;
        align-vertical: middle;
        align-horizontal: center;
        content-align: center middle;
        text-align: center;
    }
    PopUpWindow FillLabel {
        width: auto;
        height: 1;
    }
    """
    def __init__(
        self,
        *children: Widget,
        title: Optional[str]=None,
        name: Optional[str]=None,
        id: Optional[str]=None,
        classes: Optional[str]=None,
        disabled: bool=False
    ) -> None:
        self.__title = title or self.__class__.__name__
        self.__title_label = Label(self.__title)
        super().__init__(
            self.__title_label,
            FillLabel('─'),
            *children,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled
        )
    
    # ! Propertys
    @property
    def title(self) -> str:
        return self.__title
    
    @title.setter
    def title(self, value: str) -> str:
        self.__title = str(value)
        self.__title_label.update(self.__title)