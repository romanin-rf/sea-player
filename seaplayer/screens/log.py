from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.binding import Binding
from textual.widgets import Header, Footer
# > Local Imports
from seaplayer.units import logger, ll

# ! Log Screen Class

class LogScreen(Screen):
    BINDINGS = [
        Binding('escape', 'app.pop_screen', ll.get('configurate.footer.back'), priority=True),
    ]
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield logger
        yield Footer()