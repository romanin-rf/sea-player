import os
import time
import asyncio
import nest_asyncio
from pypresence import Presence, DiscordNotFound, PipeClosed, ResponseTimeout
from seaplayer.plug import PluginBase

# ! Initialization
nest_asyncio.apply()

# ! Main Class
class RichDiscordStatus(PluginBase):
    async def get_status(self):
        data = {
            "start": self.start_time,
            "large_image": "icon",
            "buttons": [{"label": "GitHub", "url": self.info.url}]
        }
        if self.app.currect_sound is not None:
            if (self.app.currect_sound.title is not None) and (self.app.currect_sound.artist is not None):
                data["details"] = f"{self.app.currect_sound.artist} - {self.app.currect_sound.title}"
            else:
                data["details"] = os.path.basename(self.app.currect_sound.name)
            if self.app.currect_sound.paused:
                data["small_image"] = "pause"
                data["small_text"] = "Paused"
            elif self.app.currect_sound.playing:
                data["small_image"] = "play"
                data["small_text"] = "Playning"
            else:
                data["small_image"] = "stop"
                data["small_text"] = "Stoped"
        else:
            data["details"] = "<unknown>"
            data["small_image"] = "question"
            data["small_text"] = "Sount not selected"
        return data
    
    async def __status__(self) -> None:
        while self.running:
            try:
                rpc = Presence("1178379471124955217")
                rpc.connect()
                while self.running:
                    data = await self.get_status()
                    rpc.update(**data)
                    await asyncio.sleep(1)
            except (DiscordNotFound, PipeClosed, ResponseTimeout):
                await asyncio.sleep(3)
    
    def on_init(self) -> None:
        self.running = False
    
    def on_run(self) -> None:
        self.start_time = time.time()
    
    async def on_compose(self):
        self.running = True
        self.worker = self.app.run_worker(
            self.__status__,
            "Rich Discord Status",
            "seaplayer.plugins.discord.status",
            thread=True
        )
    
    async def on_quit(self) -> None:
        self.running = False
        await self.worker.wait()

# ! Registration Plugin Class
__plugin__ = RichDiscordStatus