from rich.text import TextType
from rich.console import RenderableType
from textual.widgets import RadioButton
# > Typing
from typing_extensions import (
    Optional,
    Generic, 
    _T as T
)

# ! Radio Item Class

class RadioItem(RadioButton, Generic[T]):
    def __init__(self,
        label: TextType="",
        value: bool=False,
        button_first: bool=True,
        data: T=None,
        *,
        name: Optional[None]=None,
        id: Optional[str]=None,
        classes: Optional[str]=None,
        disabled: bool=False,
        tooltip: Optional[RenderableType]=None
    ) -> None:
        self.data: T = data
        super().__init__(
            label, value, button_first, 
            name=name, id=id, classes=classes, disabled=disabled, tooltip=tooltip
        )