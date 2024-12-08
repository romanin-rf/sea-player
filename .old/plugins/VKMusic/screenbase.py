from textual.screen import Screen
from textual.binding import _Bindings, Binding
from typing import List

# ! Main Class
class SeaScreen(Screen):
    DEFAULT_CSS = """
    SeaScreen {
        align-horizontal: center;
        align-vertical: middle;
    }
    """
    
    @property
    def bindings(self) -> List[Binding]:
        return self._bindings.shown_keys
    @bindings.setter
    def bindings(self, value: List[Binding]) -> None:
        self.BINDINGS = value
        self._bindings = _Bindings(value)