from uuid import UUID
from textual.widgets import Label, ListView, ListItem

# ! Playlist Item Widget Class

class PlayListItem(ListItem):
    DEFAULT_CSS = """
    PlaylistItem {
        width: 1fr;
        height: 3;
    }
    PlayListItem .first {
        height: 1;
        color: #cacaca;
        padding-left: 2;
    }
    PlayListItem .second {
        height: 1;
        color: #a9a9a9;
        padding-left: 4;
    }
    PlayListItem .third {
        height: 1;
        color: #0F0F0F;
        padding-left: 4;
    }
    """
    
    def __init__(self,
        uuid: UUID,
        first: str = '',
        second: str = '',
        third: str = '',
        *,
        name: str = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False
    ) -> None:
        self.uuid = uuid
        self.label_first, self.label_second, self.label_third = \
            Label(first, classes='first'), \
            Label(second, classes='second'), \
            Label(third, classes='third')
        super().__init__(
            self.label_first, self.label_second, self.label_third,
            name=name, id=id, classes=classes, disabled=disabled
        )
    
    def update_labels(self,
        first: str | None = None,
        second: str | None = None,
        third: str | None = None
    ) -> None:
        if first is not None:
            self.label_first.renderable = first
        if second is not None:
            self.label_second.renderable = second
        if third is not None:
            self.label_third.renderable = third

# ! Playlist View Widget Class

class PlayListView(ListView):
    def select(self, index: int) -> None:
        if 0 <= index < len(self._nodes):
            self.index = index
            selected_child = self.highlighted_child
            if selected_child is None:
                return
            self.post_message(self.Selected(self, selected_child))
    
    def select_next(self) -> None:
        if self.index is None:
            return
        index = self.index + 1
        if index >= len(self._nodes):
            index = 0
        self.index = index
        selected_child = self.highlighted_child
        if selected_child is None:
            return
        self.post_message(self.Selected(self, selected_child))
    
    def select_previous(self) -> None:
        if self.index is None:
            return
        index = self.index - 1
        if index < 0:
            index = len(self._nodes) - 1
        self.index = index
        selected_child = self.highlighted_child
        if selected_child is None:
            return
        self.post_message(self.Selected(self, selected_child))
    
    async def create_item(self,
        uuid: UUID,
        first: str = '',
        second: str = '',
        third: str = ''
    ) -> None:
        await self.append(PlayListItem(uuid, first, second, third))
