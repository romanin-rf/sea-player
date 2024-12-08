import base64
import platform
# > Graphics
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static

# ! Constants
TEXT = b'CkFuIGVycm9yIGhhcyBvY2N1cnJlZC4gVG8gY29udGludWU6CgpQcmVzcyBFbnRlciB0byByZXR1cm4gdG8ge3N5c3RlbX0sIG9yCgpQcmVzcyBDVFJMK0FMVCtERUwgdG8gcmVzdGFydCB5b3VyIGNvbXB1dGVyLiBJZiB5b3UgZG8gdGhpcywKeW91IHdpbGwgbG9zZSBhbnkgdW5zYXZlZCBpbmZvcm1hdGlvbiBpbiBhbGwgb3BlbiBhcHBsaWNhdGlvbnMuCgpFcnJvcjogMEUgOiAwMTZGIDogQkZGOUIzRDQK'
TEXT = base64.b64decode(TEXT).decode(errors="ignore").format(system=platform.system())
UNKNOWN_OPEN_KEY = base64.b64decode(b"Yg==").decode(errors="ignore")

# ! Main Class
class Unknown(Screen):
    """This Unknown screen."""
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def compose(self) -> ComposeResult:
        yield Static(f" {platform.system()} ", id="unknown-title")
        yield Static(TEXT)
        yield Static("Press any key to continue [blink]_[/]", id="unknown-any-key")