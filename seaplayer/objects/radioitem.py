from rich.text import TextType
from rich.console import RenderableType
from textual.widgets import RadioButton
# > Typing
from typing_extensions import (
    Generic, 
    _T as T
)

# ! Radio Item Class

class RadioItem(RadioButton, Generic[T]):
    def __init__(self,
        label: TextType = '',
        value: bool = False,
        button_first: bool = True,
        data: T = None,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
        tooltip: RenderableType | None = None
    ) -> None:
        self.data: T = data
        super().__init__(
            label, value, button_first, 
            name=name, id=id, classes=classes, disabled=disabled, tooltip=tooltip
        )