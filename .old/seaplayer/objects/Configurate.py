from textual.containers import ScrollableContainer, Container
# > Typing
from typing import Optional, Union

# ! Child Class
class ConfigurateListItem(Container):
    DEFAULT_CSS = """
    ConfigurateListItem {
        border: solid dodgerblue;
        background: #0000;
        border-title-color: #aaaaaa;
        border-subtitle-color: #6b6b6b;
        height: auto;
    }
    """
    
    def __init__(
        self,
        *children,
        title: str="",
        desc: str="",
        width: Union[int, str]="1fr",
        height: Union[int, str]="1fr",
        **kwargs
    ) -> None:
        super().__init__(*children, **kwargs)
        self.border_title = title
        self.border_subtitle = desc
        self.styles.width = width
        self.styles.height = height
    
    async def updating(self, title: Optional[str]="", desc: Optional[str]="") -> None:
        if title is not None: self.border_title = title
        if desc is not None: self.border_subtitle = desc

# ! Main Class
class ConfigurateList(ScrollableContainer):
    DEFAULT_CSS = """
    ConfigurateList {
        border: solid cadetblue;
        height: 1fr;
        width: 1fr;
    }
    """
    
    def __init__(self, *children, **kwargs) -> None:
        super().__init__(*children, **kwargs)
