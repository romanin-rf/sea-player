from textual import on
from textual.binding import Binding
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Input, Label
from seaplayer.objects import ClickableLabel
from seaplayer.functions import awrap
from vkpymusic import Service
from typing import Optional
from .screenbase import SeaScreen
from .widgets import SongList, SongListItem
from .units import VKM_TEXT_RANGE_OFFSET_FORMAT

# ! Main Class
class VKMScreen(SeaScreen):
    def compose(self) -> ComposeResult:
        self.bindings = [Binding("escape", "app.pop_screen", self.app.ll.get("configurate.footer.back"))]
        self.service: Optional[Service] = self.app.env['seaplayer']['codecs_kwargs'].get('vkm_service', None)
        self.songs = SongList()
        self.input_song_name = Input(placeholder="Search...", id="vkmisn")
        yield Header()
        yield self.input_song_name
        yield self.songs
        yield Footer()
    
    async def send_handlered_values(self, value: str) -> None:
        self.run_worker(
            awrap(self.app.adding_sounds_handler, value),
            name="VKM Sound Loading",
            group="vkm-temp",
            description="Loading sounds to the SeaPlayer."
        )
    
    async def input_song_name_sumbit(self, value: str) -> None:
        await self.songs.remove_children()
        for idx, song in enumerate(self.service.search_songs_by_text(value, 50)):
            handher_value = VKM_TEXT_RANGE_OFFSET_FORMAT.format(
                text=value,
                count=1,
                offset=idx
            )
            clm = awrap(self.send_handlered_values, handher_value)
            await self.songs.mount(
                SongListItem(ClickableLabel("  +  ", clm), Label(f"│ {song.artist} - {song.title} / {song.duration} sec"))
            )
    
    @on(Input.Submitted, "#vkmisn")
    async def isn(self) -> None:
        value = self.input_song_name.value
        self.input_song_name.value = ""
        if len(value.replace(" ", "")) > 0:
            if self.service is not None:
                self.app.run_worker(
                    awrap(self.input_song_name_sumbit, value),
                    group="vkm"
                )