from rich.console import Console
from textual.widgets import RichLog
# > Typing
from typing import TypeVar
# > Local Import's
from ..functions import rich_exception

# ! Vars
console = Console()

# ! Main Class
class LogMenu(RichLog):
    DEFAULT_CSS = """
    LogMenu {
        background: $surface;
        color: $text;
        height: 75vh;
        dock: bottom;
        layer: notes;
        border-top: hkey $primary;
        offset-y: 0;
        transition: offset 400ms in_out_cubic;
        padding: 0 1 1 1;
    }
    LogMenu:focus {
        offset: 0 0 !important;
    }
    LogMenu.--hidden {
        offset-y: 100%;
    }
    """
    
    def __init__(self, chap_max_width: int=8, enable_logging: bool=True, **kwargs):
        self.enable_logging = enable_logging
        self.chap_max_width = chap_max_width
        if (classes:=kwargs.get("classes", None)) is None:
            kwargs["classes"] = "--hidden"
        else:
            kwargs["classes"] = f"{classes} --hidden"
        super().__init__(**kwargs)
    
    def write_log(self, chap: str, msg: str, *, chap_color: str="green", in_console: bool=False) -> None:
        if self.enable_logging:
            text = f"[[{chap_color}]{chap.center(self.chap_max_width)}[/]]: {msg}"
            self.write(text, shrink=False)
            if in_console:
                console.print(text)
    
    def info(self, msg: str, *, in_console: bool=False) -> None:
        self.write_log("INFO", msg, chap_color="green", in_console=in_console)
    
    def error(self, msg: str, *, in_console: bool=False) -> None:
        self.write_log("ERROR", msg, chap_color="red", in_console=in_console)
    
    def warn(self, msg: str, *, in_console: bool=False) -> None:
        self.write_log("WARN", msg, chap_color="orange", in_console=in_console)
    
    def exception(self, e: Exception, *, in_console: bool=False) -> None:
        self.write_log("ERROR", rich_exception(e), chap_color="red", in_console=in_console)
