import os
import glob
from uuid import UUID
from textual import on, work
from textual.app import App, ComposeResult
from textual.worker import Worker, WorkerCancelled, WorkerFailed
from textual.widgets import Label, Input, Button, Header, Footer, ListView
from textual.containers import Container, Vertical, Horizontal
# > SeaPlayer (Audio)
from seaplayer_audio import AsyncCallbackSoundDeviceStreamer
# > Pillow
from PIL import Image
# > Typing
from typing_extensions import (
    List,
    Type
)
# > Local Imports (Types)
from ._types import PlaybackMode, SupportAudioStreamer
# > Local Imports (seaplayer)
from .track import Track, PlaybackerState, Playbacker
from .input_handler import InputHandlerBase, FileGlobInputHandler
# > Local Imports (Units)
from .units import (
    __title__, __version__,
    CSS_LOCALDIR, LANGUAGES_DIRPATH, CACHE_DIRPATH, CONFIG_FILEPATH,
    IMG_NOT_FOUND
)
# > Local Imports (Main)
from .config import Config
from .languages import LanguageLoader
# > Local Imports (TUI)
from .objects.agt import AnimatedGradientText
from .objects.progressbar import PlaybackProgress
from .objects.image import ImageWidget
from .objects.playlist import PlayListView, PlayListItem
from .objects.separator import HorizontalSeporator
# > Local Imports (Spetific)
from .others.cache import Cacher

# ! Template Variables

def null_widget(text: str):
    yield from []
    yield AnimatedGradientText( text )

# ! SeaPlayer Main Application
class SeaPlayer(App[int]):
    # ^ Main Settings
    TITLE = f"{__title__} v{__version__}"
    ENABLE_COMMAND_PALETTE = False
    CSS_PATH = [
        os.path.join(CSS_LOCALDIR, "seaplayer.tcss"),
        #os.path.join(CSS_LOCALDIR, "configurate.tcss"),
    ]
    
    # ^ Runtime Constants
    
    INPUT_HANDLERS_TYPES: List[Type[InputHandlerBase]] = [ FileGlobInputHandler ]
    INPUT_HANDLERS: List[InputHandlerBase] = []
    
    # ^ Runtime Variables
    
    config: Config = Config(CONFIG_FILEPATH)
    cacher: Cacher = Cacher(CACHE_DIRPATH)
    ll: LanguageLoader = LanguageLoader(LANGUAGES_DIRPATH, config.main_language)
    
    # ^ Playback Variables
    
    streamer: SupportAudioStreamer
    playbacker: Playbacker
    playback_mode = cacher.var('playback_mode', PlaybackMode.PLAY)
    
    # ^ Dunder Methods
    
    # ^ Spetific Methods
    
    def get_playback_mode_text(self) -> str:
        return self.ll.get(f"player.button.mode.{self.playback_mode.name.lower()}")
    
    def get_playback_statuses_text(self) -> str:
        # TODO: Написать получение данных о текущем статусе воспроизведения
        return f"00:00 | {round(self.playbacker.volume*100):>3}%", None, None
    
    # ^ Workers
    
    async def worker_input_submitted(self, inputted: str) -> None:
        for handler in self.INPUT_HANDLERS:
            if handler.is_this(inputted):
                for track_uuid in handler.handle(inputted):
                    self.call_from_thread(
                        self.playlist_view.create_item,
                        track_uuid,
                        self.playbacker.tracks[track_uuid].__playback_name__(),
                        self.playbacker.tracks[track_uuid].__playback_subtitle__(),
                    )
    
    async def worker_track_selected(self, uuid: UUID) -> None:
        await self.playbacker.select_by_uuid(uuid)
        if self.playbacker.selected_track is not None:
            await self.player_image.update_image(self.playbacker.selected_track.cover)
    
    # ^ On Methods
    
    @on(Button.Pressed, "#switch-playback-mode")
    async def switch_playback_mode(self, event: Button.Pressed) -> None:
        if self.playback_mode == PlaybackMode.PLAY:
            self.playback_mode = PlaybackMode.REPLAY_SOUND
        elif self.playback_mode == PlaybackMode.REPLAY_SOUND:
            self.playback_mode = PlaybackMode.REPLAY_LIST
        else:
            self.playback_mode = PlaybackMode.PLAY
        self.player_playback_switch_button.label = self.get_playback_mode_text()
    
    @on(Button.Pressed, "#button-pause")
    async def pause_playback(self, event: Button.Pressed) -> None:
        # TODO: Написать метод паузы воспроизведения
        if self.playbacker.selected_track is None:
            return
    
    @on(Button.Pressed, "#button-play-stop")
    async def play_or_stop_playback(self, event: Button.Pressed) -> None:
        # TODO: Написать метод воспроизведения или остановки воспроизведения
        if self.playbacker.selected_track is None:
            return
    
    @on(Input.Submitted, "#soundinput")
    async def sound_input_submitted(self, event: Input.Submitted) -> None:
        inputted = event.value.strip()
        if len(inputted) == 0:
            return
        event.input.clear()
        self.run_worker(
            self.worker_input_submitted(inputted),
            name='Input Submitted Handler',
            group='seaplayer.main',
            thread=True,
        )
    
    @on(PlayListView.Selected, ".playlist-container")
    async def sound_selected(self, event: PlayListView.Selected) -> None:
        plitem: PlayListItem = event.item
        self.run_worker(
            self.worker_track_selected(plitem.uuid),
            name='Track Selected Work',
            group='seaplayer.main',
            thread=True,
        )
    
    # ^ Compose Method
    
    def compose(self) -> ComposeResult:
        # * Play Screen
        
        self.player_box = Container(classes="player-box")
        self.player_box.border_title = self.ll.get("player")
        
        # * Image Object Init
        
        self.player_selected_label = next(null_widget('<Label: DEV>'))#Label("<None>", classes="player-selected-label")
        self.player_image = ImageWidget(IMG_NOT_FOUND, resample=Image.Resampling.BILINEAR)
        
        # * Compositions Screen
        
        self.playlist_box = Container(classes="playlist-box")
        self.playlist_box.border_title = self.ll.get("playlist")
        self.playlist_view = PlayListView(classes="playlist-container")
        
        self.playlist_sound_input = Input(
            classes="playlist-sound-input", id="soundinput",
            placeholder=self.ll.get("playlist.input.placeholder")
        )
        self.player_playback_switch_button = Button(
            self.get_playback_mode_text(),
            id="switch-playback-mode",
            variant="primary",
            classes="button-sound-control"
        )
        
        # * Compose
        
        yield Header()
        with self.player_box:
            with Vertical():
                with Container(classes="player-visual-panel"):
                    yield self.player_image
                with Container(classes="player-contol-panel"):
                    yield self.player_selected_label
                    yield PlaybackProgress(getfunc=self.get_playback_statuses_text)
                    with Horizontal(classes="box-buttons-sound-control"):
                        yield Button(
                            self.ll.get("player.button.pause"),
                            id="button-pause",
                            variant="success",
                            classes="button-sound-control"
                        )
                        yield Button(
                            self.ll.get("player.button.psu"),
                            id="button-play-stop",
                            variant="warning",
                            classes="button-sound-control"
                        )
                        yield self.player_playback_switch_button
        with self.playlist_box:
            yield self.playlist_view
            yield HorizontalSeporator()
            yield self.playlist_sound_input
        yield Footer()
    
    async def on_ready(self) -> None:
        for input_handler_type in self.INPUT_HANDLERS_TYPES:
            self.INPUT_HANDLERS.append(input_handler_type(self.playbacker))
    
    async def on_run(self) -> None:
        self.streamer = AsyncCallbackSoundDeviceStreamer()
        self.playbacker = Playbacker(self.streamer, volume=1.0)
        await self.streamer.start()
    
    # ^ Textaul Actions
    
    async def action_quit(self):
        await self.streamer.stop()
        return await super().action_quit()
    
    # ^ Textual Methods
    
    async def run_async(self, *args, **kwargs):
        await self.on_run()
        return await super().run_async(*args, **kwargs)