from pydantic import BaseModel
from textual.binding import Binding
from textual.screen import Screen
# > Typing
from typing import Optional, Generator, Type, Callable, List, Any
# > Local Import's
from ..codeсbase import CodecBase
from ..functions import formater

# ! Plugin Info Class
class PluginInfo(BaseModel):
    name: str
    name_id: str
    version: str
    author: str
    description: Optional[str]=None
    url: Optional[str]=None

# ! Plugin Base Class
class PluginBase:
    def __init_repr__(self) -> str:
        return f"{self.info.name} ({repr(self.info.name_id)}) [#60fdff]v{self.info.version}[/#60fdff] is [yellow]initialized[/yellow]!"
    
    def __init__(self, app, pl, info: PluginInfo) -> None:
        self.app = app
        self.pl = pl
        self.info = info
        # > Logs
        self.app.info(self.__init_repr__())
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({formater(info=self.info)})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    # ! App Specific Functions
    def install_screen(self, name: str, screen: Screen) -> None:
        self.app.SCREENS[name] = screen
        self.app.install_screen(screen, name)
    
    def add_codecs(self, *codecs: Type[CodecBase]) -> None:
        self.app.env['seaplayer']['codecs'] += list(codecs)
    
    def add_value_handlers(self, *handlers: Callable[[str], List[str]]) -> None:
        self.pl.value_handlers += list(handlers)
    
    # ! Dev Functions
    def on_bindings(self) -> Generator[Binding, Any, None]:
        yield
    
    def on_init(self):
        pass
    
    def on_run(self):
        pass
    
    async def on_compose(self):
        pass
    
    async def on_ready(self):
        pass
    
    async def on_quit(self):
        pass
