import os
import time
from uuid import UUID
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding, BindingType
from textual.widgets import Label, Input, Button, Header, Footer
from textual.containers import Container, Vertical, Horizontal
# > Typing
from typing_extensions import (
    List,
    Iterator,
    Type
)
# > Local Imports (Types)
from seaplayer._types import PlaybackMode
# > Local Imports (seaplayer)
from seaplayer.track import PlaybackerState, Playbacker, PlaybackerChangeStateMessage, PlaybackerTrackEndMessage
from seaplayer.input_handler import InputHandlerBase, FileGlobInputHandler
# > Local Imports (Units)
from seaplayer.units import (
    ll, config, cacher, logger,
    __title__, __version__,
    CSS_LOCALDIR,
    IMG_NOT_FOUND
)
# > Local Imports (Main)
from seaplayer.config import Config
from seaplayer.languages import LanguageLoader
from seaplayer.screens import SCREENS as APP_SCREENS, screens_bindings as app_screens_bindings
# > Local Imports (TUI)
from seaplayer.objects.log import TextualLogLevel
from seaplayer.objects.image import ImageWidget
from seaplayer.objects.progressbar import PlaybackProgress
from seaplayer.objects.playlist import PlayListView, PlayListItem
from seaplayer.objects.separator import HorizontalSeporator
# > Local Imports (Others)
from seaplayer.others.timer import Timer

# ! Template Variables

def generate_bindings(config: Config, ll: LanguageLoader) -> Iterator[BindingType]:
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
    yield from app_screens_bindings(config, ll)

# ! SeaPlayer Main Application
class SeaPlayer(App):
    # ^ Main Settings
    TITLE = f"{__title__} v{__version__}"
    CSS_PATH = [
        os.path.join(CSS_LOCALDIR, "seaplayer.tcss"),
    ]
    BINDINGS = list(generate_bindings(config, ll))
    ENABLE_COMMAND_PALETTE = False
    SCREENS = APP_SCREENS
    
    # ^ Runtime Constants
    
    INPUT_HANDLERS_TYPES: List[Type[InputHandlerBase]] = [
        FileGlobInputHandler
    ]
    INPUT_HANDLERS: List[InputHandlerBase] = []
    
    # ^ Playback Variables
    
    playbacker: Playbacker
    playback_mode = cacher.var('playback_mode', PlaybackMode.PLAY)
    
    # ^ Textual Spetific Methods
    
    async def action_smart_push_screen(self, screen: str) -> None:
        if self.get_screen(screen).is_current:
            return
        return await super().action_push_screen(screen)
    
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
    
    def refresh_selected_label(self) -> None:
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
        self.player_status_label.update(
            '<{0}> {1}'.format(
                ll.get(key),
                self.playbacker.selected_track.__playback_name__()
            )
        )
    
    # ^ Workers
    
    async def worker_input_submitted(self, inputted: str) -> None:
        for handler in self.INPUT_HANDLERS:
            if handler.is_this(inputted):
                logger.group('(START) ADDING TRACKS', TextualLogLevel.TRACE)
                added = 0
                with Timer() as timer:
                    for track_uuid in handler.handle(inputted):
                        self.call_from_thread(
                            self.playlist_view.create_item,
                            track_uuid,
                            self.playbacker.tracks[track_uuid].__playback_name__(),
                            self.playbacker.tracks[track_uuid].__playback_subtitle__(),
                        )
                        added += 1
                        logger.trace('Added track: ' + str(self.playbacker.tracks[track_uuid]))
                logger.debug(ll.get('nofys.sound.added').format(added, count=added))
                logger.debug(f'[green]Time[/green]: {str(timer)} second(s)')
                logger.group('(END) ADDING TRACKS', TextualLogLevel.TRACE)
                self.notify(ll.get('nofys.sound.added').format(added, count=added), timeout=2)
    
    async def worker_track_selected(self, uuid: UUID) -> None:
        self.playbacker.stop()
        self.playbacker.select_by_uuid(uuid)
        if self.playbacker.selected_track is not None:
            logger.trace(f'Track selected: {self.playbacker.selected_track}')
            if self.playbacker.streamer.samplerate != self.playbacker.selected_track.source.samplerate:
                with Timer() as timer:
                    self.playbacker.reconfigurate(self.playbacker.selected_track.source.samplerate)
                logger.debug(f'[green]Reconfigurate Time[/green]: {str(timer)} second(s)')
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
    
    @on(PlaybackerTrackEndMessage)
    def sound_track_ended(self, event: PlaybackerTrackEndMessage) -> None:
        pass
    
    # ^ Compose Method
    
    def compose(self) -> ComposeResult:
        # * Play Screen
        
        self.player_box = Container(classes="player-box")
        self.player_box.border_title = ll.get("player")
        
        # * Image Object Init
        
        self.player_status_label = Label('<{0}>'.format(ll.get('sound.status.none')), classes="player-selected-label")
        self.player_image = ImageWidget(
            IMG_NOT_FOUND, 
            resample=config.image.resample,
            render_mode=config.image.render_mode
        )
        
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
                    yield self.player_status_label
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
            if new_position >= 0.0:
                self.playbacker.selected_track.set_position(new_position)
            else:
                self.playbacker.selected_track.set_position(0.0)
    
    async def action_volume_add(self) -> None:
        new_volume = round(self.playbacker.volume + config.sound.volume_per, 2)
        if config.sound.max_volume >= new_volume:
            self.playbacker.volume = new_volume
    
    async def action_volume_drop(self) -> None:
        new_volume = round(self.playbacker.volume - config.sound.volume_per, 2)
        if new_volume >= 0.0:
            self.playbacker.volume = new_volume
    
    async def nothing(self) -> None:
        pass
    
    # ^ Textaul Actions
    
    async def on_run(self) -> None:
        self.playbacker = Playbacker(self, device_id=config.main.device_id)
    
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
        return await super().run_async(*args, **kwargs)