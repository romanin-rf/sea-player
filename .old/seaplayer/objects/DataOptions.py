from textual.widgets import OptionList
from textual.widgets.option_list import Option
# > Typing
from typing import Optional, Callable

# ! Child Class
class DataOption(Option):
    def __init__(
        self,
        text: str,
        selected: bool=False,
        id: Optional[str]=None,
        disable: bool=False,
        **data
    ) -> None:
        super().__init__(text, id=id, disabled=disable)
        self.group = ""
        self.selected = selected
        self.data = data

# ! Main Class
class DataOptionList(OptionList):
    def __init__(
        self,
        *content: DataOption,
        group: Optional[str]="",
        after_selected: Callable[[DataOption], None]=lambda option: None
    ) -> None:
        super().__init__()
        self.group = group
        self.content = content
        self.after_selected = after_selected
    
    def on_mount(self):
        for index, option in enumerate(self.content):
            self.add_option(option)
            if isinstance(option, DataOption):
                option.group = self.group
                if option.selected:
                    self.highlighted = index
    
    async def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if isinstance(event.option, DataOption):
            if self.group == event.option.group:
                await self.after_selected(event.option)
