from textual.app import RenderResult
from textual.widgets.option_list import Option
# > Typing
from typing_extensions import (
    Generic, 
    _T as T
)

# ! Option Item Class

class OptionItem(Option, Generic[T]):
    def __init__(self,
        prompt: RenderResult,
        data: T,
        id: str | None = None,
        disabled: bool = False
    ) -> None:
        self.data: T = data
        super().__init__(prompt, id, disabled)