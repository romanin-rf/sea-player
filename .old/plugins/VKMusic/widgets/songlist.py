from textual.containers import VerticalScroll, Horizontal

# ! Children
class SongListItem(Horizontal):
    DEFAULT_CSS = """
    SongListItem {
        width: 1fr;
        height: 1;
    }
    """

# ! Main Class
class SongList(VerticalScroll):
    DEFAULT_CSS = """
    SongList {
        height: 1fr;
        width: 1fr;
        border: solid dodgerblue;
    }
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.border_title = "Songs"