import os
import glob
from textual import on, work
from textual.app import App, ComposeResult
from textual.widgets import Label, Input, Button, Header, Footer
from textual.containers import Container, Vertical, Horizontal
# > SeaPlayer (Audio)
from seaplayer_audio import AsyncCallbackSoundDeviceStreamer
# > Pillow
from PIL import Image
# > Typing
from typing_extensions import (
    List
)
# > Local Imports (Types)
from ._types import PlaybackMode, SupportAudioStreamer
# > Local Imports (seaplayer)
from .track import Track, PlaybackerState, Playbacker
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
        #os.path.join(CSS_LOCALDIR, "unknown.tcss"),
        #os.path.join(CSS_LOCALDIR, "objects.tcss")
    ]
    
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
    
    def _globpath(self, path: str) -> List[str]:
        filepaths = []
        for filepath in glob.glob(path, recursive=True):
            if not self.playbacker.exists_track_by_input(filepath):
                filepaths.append(os.path.abspath(filepath))
        return filepaths
    
    # ^ Workers
    
    # // Code...
    
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
        # TODO: Написать метод отправки на обработку input-а
        event.input.clear()
        values = self._globpath()
        if len(values) == 0:
            return
        
    
    # ^ Compose Method
    
    def compose(self) -> ComposeResult:
        # * Play Screen
        
        self.player_box = Container(classes="player-box")
        self.player_box.border_title = self.ll.get("player")
        
        # * Image Object Init
        
        self.player_selected_label = next(null_widget('<Label: DEV>'))#Label("<None>", classes="player-selected-label")
        self.player_image = ImageWidget(IMG_NOT_FOUND)
        
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
        await self.playlist_view.extend(
            [
                PlayListItem(
                    None,
                    'NBSPLV - Spectate',
                    '44100 Hz, Stereo, 360 kbps, MP3'
                ),
                PlayListItem(
                    None,
                    'NBSPLV - Downpour',
                    '48000 Hz, Stereo, 1260 kbps, FLAC'
                ),
                PlayListItem(
                    None,
                    'NBSPLV - Algorithm',
                    '44100 Hz, Mono, 128 kbps, WAV'
                )
            ]
        )
    
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