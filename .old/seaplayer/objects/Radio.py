from textual.widgets import RadioSet, RadioButton
# > Typing
from typing import Optional, Callable, Generic, TypeVar

# ! Types
DT = TypeVar("DT")

# ! Data Radio Button Class
class DataRadioButton(RadioButton, Generic[DT]):
    def __init__(self, data: DT, value: bool=False, visible_data: Optional[str]=None) -> None:
        self.data = data
        self.visible_data = visible_data or str(data)
        super().__init__(visible_data, value)

# ! Data Radio Set Class
class DataRadioSet(RadioSet, Generic[DT]):
    def __init__(
        self,
        on_changed: Callable[[DT], None],
        *buttons: DataRadioButton[DT],
        **kwargs
    ) -> None:
        super().__init__(*buttons, **kwargs)
        self.__on_changed_method = on_changed
    
    def _on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        super()._on_radio_set_changed(event)
        self.__on_changed_method(event.pressed.data)

