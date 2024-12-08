from textual.screen import Screen
from seaplayer.seaplayer import SeaPlayer
from textual.binding import Binding
from typing import List

# ! Main Class
class SeaScreen(Screen):
    app: SeaPlayer
    
    @property
    def bindings(self) -> List[Binding]: ...
    @bindings.setter
    def bindings(self, value: List[Binding]) -> None: ...