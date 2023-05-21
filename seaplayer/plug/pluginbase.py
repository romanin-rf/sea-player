from pydantic import BaseModel
# > Local Import's
from typing import Optional

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
    def __init__(self, app, pl, info) -> None:
        self.app = app
        self.pl = pl
        self.info = info
    
    async def on_pre_init(app, pl) -> None: ...
    async def on_init(self) -> None: ...
    async def on_start(self) -> None: ...
    async def on_quit(self) -> None: ...
