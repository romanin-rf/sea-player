import os
from uuid import UUID
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Label, Input, Button, Header, Footer
from textual.containers import Container, Vertical, Horizontal
# > Pillow
from PIL import Image
# > Typing
from typing_extensions import (
    List,
    Type
)
# > Local Imports (Types)
from ._types import PlaybackMode
# > Local Imports (seaplayer)
from .track import PlaybackerState, Playbacker, PlaybackerChangeStateMessage
from .input_handler import InputHandlerBase, FileGlobInputHandler
# > Local Imports (Units)
from .units import (
    ll, config, cacher,
    __title__, __version__,
    CSS_LOCALDIR,
    IMG_NOT_FOUND
)
# > Local Imports (Main)
from .config import Config
from .languages import LanguageLoader
# > Local Imports (TUI)
from .objects.progressbar import PlaybackProgress
from .objects.image import ImageWidget
from .objects.playlist import PlayListView, PlayListItem
from .objects.separator import HorizontalSeporator

# ! Template Variables

def generate_bindings(config: Config, ll: LanguageLoader):
    yield Binding(config.key.quit, "quit", ll.get("footer.quit"))
    yield Binding(
        config.key.volume_add, "volume_add",
        ll.get("footer.volume.plus") \
            .format(per=round(config.sound.volume_per*100))
    )
    yield Binding(
        config.key.volume_drop, "volume_drop",
        ll.get("footer.volume.minus") \
            .format(per=round(config.sound.volume_per*100))
    )
    yield Binding(
        config.key.rewind_backward, "rewind_backward",
        ll.get("footer.rewind.minus") \
            .format(sec=config.sound.rewind_per)
    )
    yield Binding(
        config.key.rewind_forward, "rewind_forward",
        ll.get("footer.rewind.plus") \
            .format(sec=config.sound.rewind_per)
    )

# ! SeaPlayer Main Application
class SeaPlayer(App):
    # ^ Main Settings
    TITLE = f"{__title__} v{__version__}"
    CSS_PATH = [
        os.path.join(CSS_LOCALDIR, "seaplayer.tcss"),
    ]
    BINDINGS = list(generate_bindings(config, ll))
    ENABLE_COMMAND_PALETTE = False
    
    # ^ Runtime Constants
    
    INPUT_HANDLERS_TYPES: List[Type[InputHandlerBase]] = [ FileGlobInputHandler ]
    INPUT_HANDLERS: List[InputHandlerBase] = []
    
    # ^ Playback Variables
    
    playbacker: Playbacker
    playback_mode = cacher.var('playback_mode', PlaybackMode.PLAY)
    
    # ^ Spetific Methods
    
    def get_playback_mode_text(self) -> str:
        return ll.get(f"player.button.mode.{self.playback_mode.name.lower()}")
    
    async def get_playback_statuses_text(self) -> str:
        if self.playbacker.selected_track is not None:
            position = self.playbacker.selected_track.get_position()
            duration = self.playbacker.selected_track.duration
            cm, cs, vol, tm, ts = \
                round(position // 60), round(position % 60), \
                round(self.playbacker.volume * 100), \
                round(duration // 60), round(duration % 60)
            text = f"{cm:0>2}:{cs:0>2} / {tm:0>2}:{ts:0>2} | {vol:>3}%"
            return text, position, self.playbacker.selected_track.duration
        return f"00:00 / 00:00 | {round(self.playbacker.volume*100):>3}%", None, None
    
    def refresh_selected_label(self):
        if self.playbacker.selected_track is not None:
            if PlaybackerState.PLAYING in self.playbacker.state:
                if PlaybackerState.PAUSED not in self.playbacker.state:
                    key = 'sound.status.playing'
                else:
                    key = 'sound.status.paused'
            else:
                key = 'sound.status.stopped'
        else:
            key = 'sound.status.none'
        self.player_selected_label.update(
            '<{0}> {1}'.format(
                ll.get(key),
                self.playbacker.selected_track.__playback_name__()
            )
        )
    
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
        self.playbacker.stop()
        self.playbacker.select_by_uuid(uuid)
        if self.playbacker.selected_track is not None:
            if self.playbacker.streamer.samplerate != self.playbacker.selected_track.source.samplerate:
                self.playbacker.reconfigurate(self.playbacker.selected_track.source.samplerate)
            self.call_from_thread(self.player_image.update_image, self.playbacker.selected_track.cover)
        self.call_from_thread(self.refresh_selected_label)
    
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
        if (self.playbacker.selected_track is None) and (PlaybackerState.PLAYING not in self.playbacker.state):
            return
        if PlaybackerState.PAUSED in self.playbacker.state:
            self.playbacker.unpause()
        else:
            self.playbacker.pause()
    
    @on(Button.Pressed, "#button-play-stop")
    async def play_or_stop_playback(self, event: Button.Pressed) -> None:
        if self.playbacker.selected_track is None:
            return
        if PlaybackerState.PLAYING in self.playbacker.state:
            self.playbacker.stop()
        else:
            self.playbacker.play()
    
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
    
    @on(PlaybackerChangeStateMessage)
    def sound_change_state(self, event: PlaybackerChangeStateMessage) -> None:
        self.refresh_selected_label()
    
    # ^ Compose Method
    
    def compose(self) -> ComposeResult:
        # * Play Screen
        
        self.player_box = Container(classes="player-box")
        self.player_box.border_title = ll.get("player")
        
        # * Image Object Init
        
        self.player_selected_label = Label('<{0}>'.format(ll.get('sound.status.none')), classes="player-selected-label")
        self.player_image = ImageWidget(IMG_NOT_FOUND, resample=Image.Resampling.BILINEAR)
        
        # * Compositions Screen
        
        self.playlist_box = Container(classes="playlist-box")
        self.playlist_box.border_title = ll.get("playlist")
        self.playlist_view = PlayListView(classes="playlist-container")
        
        self.playlist_sound_input = Input(
            classes="playlist-sound-input", id="soundinput",
            placeholder=ll.get("playlist.input.placeholder")
        )
        self.player_playback_switch_button = Button(
            self.get_playback_mode_text(),
            id="switch-playback-mode",
            variant="primary",
            classes="button-sound-control"
        )
        
        # * Compose
        
        yield Header(icon='🌊')
        with self.player_box:
            with Vertical():
                with Container(classes="player-visual-panel"):
                    yield self.player_image
                with Container(classes="player-contol-panel"):
                    yield self.player_selected_label
                    yield PlaybackProgress(getfunc=self.get_playback_statuses_text)
                    with Horizontal(classes="box-buttons-sound-control"):
                        yield Button(
                            ll.get("player.button.pause"),
                            id="button-pause",
                            variant="success",
                            classes="button-sound-control"
                        )
                        yield Button(
                            ll.get("player.button.psu"),
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
    
    # ^ SeaPlayer Textual Actions
    
    async def action_rewind_forward(self) -> None:
        if self.playbacker.selected_track is not None:
            new_position = self.playbacker.selected_track.get_position() + config.sound.rewind_per
            if self.playbacker.selected_track.duration >= new_position:
                self.playbacker.selected_track.set_position(new_position)
    
    async def action_rewind_backward(self) -> None:
        if self.playbacker.selected_track is not None:
            new_position = self.playbacker.selected_track.get_position() - config.sound.rewind_per
            if 0.0 >= self.playbacker.selected_track.duration:
                self.playbacker.selected_track.set_position(new_position)
    
    async def action_volume_add(self) -> None:
        new_volume = round(self.playbacker.volume + config.sound.volume_per, 2)
        if config.sound.max_volume >= new_volume:
            self.playbacker.volume = new_volume
    
    async def action_volume_drop(self) -> None:
        new_volume = round(self.playbacker.volume - config.sound.volume_per, 2)
        if new_volume >= 0.0:
            self.playbacker.volume = new_volume
    
    # ^ Textaul Actions
    
    async def on_run(self) -> None:
        self.playbacker = Playbacker(self)
    
    async def on_ready(self) -> None:
        for input_handler_type in self.INPUT_HANDLERS_TYPES:
            self.INPUT_HANDLERS.append(input_handler_type(self.playbacker))
        self.playbacker.start()
    
    async def action_quit(self):
        self.playbacker.terminate()
        return await super().action_quit()
    
    # ^ App Methods
    
    async def run_async(self, *args, **kwargs):
        await self.on_run()
        return super().run_async(*args, **kwargs)