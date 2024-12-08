import os
import glob
import asyncio
# > Graphics
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding, BindingsMap
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Header, Footer, Static, Label, Button, Input, ListView
# > Image Works
from PIL import Image
# > Typing
from typing import Optional, Literal, Tuple, List, Type, Union
# > Local Imports
from .config import SeaPlayerConfig
from .types import Cacher, Environment
from .codeсbase import CodecBase
from .languages import LanguageLoader
from .screens import Unknown, Configurate, UNKNOWN_OPEN_KEY
from .codecs import codecs
from .functions import (
    aiter, awrap,
    image_from_bytes,
    get_sound_basename,
    aio_check_status_code
)
from .objects import (
    Nofy,
    LogMenu,
    CallNofy,
    PlayListView,
    AsyncImageLabel,
    StandartImageLabel,
    IndeterminateProgress
)
from .units import (
    __title__,
    __version__,
    __author__,
    __email__,
    __url__,
    CSS_LOCALDIR,
    CONFIG_FILEPATH,
    ASSETS_DIRPATH,
    IMGPATH_IMAGE_NOT_FOUND,
    RESAMPLING_SAFE,
    LOCALDIR,
    ENABLE_PLUGIN_SYSTEM,
    CACHE_DIRPATH,
    LANGUAGES_DIRPATH
)
# > Plugin System Init
if ENABLE_PLUGIN_SYSTEM:
    from .plug import PluginLoader

# ! Main Functions
def build_bindings(config: SeaPlayerConfig, ll: LanguageLoader):
    yield Binding(config.key_quit, "quit", ll.get("footer.quit"))
    yield Binding("c,с", "push_screen('configurate')", ll.get("footer.configurate"))
    if config.logging:
        yield Binding("l,д", "app.toggle_class('LogMenu', '--hidden')", ll.get("footer.logs"))
    yield Binding(config.key_rewind_back, "minus_rewind", ll.get('footer.rewind.minus').format(sec=config.rewind_count_seconds))
    yield Binding(config.key_rewind_forward, "plus_rewind", ll.get('footer.rewind.plus').format(sec=config.rewind_count_seconds))
    yield Binding(config.key_volume_down, "minus_volume", ll.get('footer.volume.minus').format(per=round(config.volume_change_percent*100)))
    yield Binding(config.key_volume_up, "plus_volume", ll.get('footer.volume.plus').format(per=round(config.volume_change_percent*100)))
    yield Binding("ctrl+s", "screenshot", ll.get('footer.screenshot'))
    yield Binding(UNKNOWN_OPEN_KEY, "push_screen('unknown')", show=False)

# ! Main
class SeaPlayer(App):
    # ! Textual Configuration
    TITLE = f"{__title__} v{__version__}"
    CSS_PATH = [
        os.path.join(CSS_LOCALDIR, "seaplayer.tcss"),
        os.path.join(CSS_LOCALDIR, "configurate.tcss"),
        os.path.join(CSS_LOCALDIR, "unknown.tcss"),
        os.path.join(CSS_LOCALDIR, "objects.tcss")
    ]
    SCREENS = {
        "unknown": Unknown(id="screen_unknown"),
        "configurate": Configurate(id="screen_configurate")
    }
    ENABLE_COMMAND_PALETTE = False
    
    # ! SeaPlayer Configuration
    cache: Cacher = Cacher(CACHE_DIRPATH)
    """An image of a class for caching variables."""
    config: SeaPlayerConfig = SeaPlayerConfig(CONFIG_FILEPATH)
    """The image of the SeaPlayer configuration file."""
    ll: LanguageLoader = LanguageLoader(LANGUAGES_DIRPATH, config.lang)
    """An image of the class for receiving the loaded SeaPlayer translation. With the translation uploaded from the `seaplayer/langs/` directory."""
    image_type: Optional[Union[Type[AsyncImageLabel], Type[StandartImageLabel]]] = None
    env = Environment(
        {
            "seaplayer": {
                "codecs": [*codecs],
                "codecs_kwargs": {
                    "sound_fonts_path": config.sound_font_path,
                    "sound_device_id": config.output_sound_device_id
                }
            }
        }
    )
    
    # ! Bindings
    BINDINGS = list(build_bindings(config, ll))
    
    # ! Template Configuration
    currect_sound: Optional[CodecBase] = None
    """The currently selected sound."""
    currect_sound_index: Optional[int] = None
    """The index of the currently selected sound."""
    currect_volume: float = cache.var("currect_volume", 1.0)
    """The current volume value (cached)."""
    last_playback_status: Optional[Literal[0, 1, 2]] = None
    playback_mode: int = cache.var("playback_mode", 0)
    """The current playback mode (cached)."""
    block_select: bool = False
    block_playback_control: bool = False
    last_handlered_values: List[str] = []
    started: bool = True
    
    # ! Init Objects
    log_menu = LogMenu(
        enable_logging=config.logging,
        wrap=True, highlight=True, markup=True
    )
    
    # ! Log Functions
    info = log_menu.info
    error = log_menu.error
    warn = log_menu.warn
    exception = log_menu.exception
    
    # ! App Init
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if ENABLE_PLUGIN_SYSTEM:
            self.plugin_loader = PluginLoader(self)
            self.plugin_loader.on_init()
            self.update_bindings()
    
    def update_bindings(self) -> None:
        bindings = list(build_bindings(self.config, self.ll))
        if ENABLE_PLUGIN_SYSTEM:
            for _binding in self.plugin_loader.on_bindings():
                if _binding is not None:
                    bindings.append(_binding)
        self._bindings = _Bindings(bindings)
    
    # ! Inherited Functions
    async def action_push_screen(self, screen: str) -> None:
        if self.SCREENS[screen].id != self.screen.id:
            await super().action_push_screen(screen)
    
    # ! Nofy's
    def nofy(
        self,
        text: str,
        life_time: float=3,
        dosk: Literal["bottom", "left", "right", "top"]="top"
    ) -> None:
        """Creating a temporary notification.
        
        Args:
            text (str): The text of the notification.
            life_time (float, optional): The time in seconds after which the notification will disappear. Defaults to 3.
            dosk (Literal[\"bottom\", \"left\", \"right\", \"top\"], optional): Regarding the screen. Defaults to "top".
        """
        self.screen.mount(Nofy(text, life_time, dosk))
    
    async def aio_nofy(
        self,
        text: str,
        life_time: float=3,
        dosk: Literal["bottom", "left", "right", "top"]="top"
    ) -> None:
        """Creating a temporary notification.
        
        Args:
            text (str): The text of the notification.
            life_time (float, optional): The time in seconds after which the notification will disappear. Defaults to 3.
            dosk (Literal[\"bottom\", \"left\", \"right\", \"top\"], optional): Regarding the screen. Defaults to "top".
        """
        await self.screen.mount(Nofy(text, life_time, dosk))
    
    def callnofy(
        self,
        text: str,
        dosk: Literal["bottom", "left", "right", "top"]="top"
    ) -> CallNofy:
        """Creating a notification.
        
        Args:
            text (str): The text of the notification.
            dosk (Literal[\"bottom\", \"left\", \"right\", \"top\"], optional): Regarding the screen. Defaults to "top".
        
        Returns:
            CallNofy: To delete the notification image, use the `CallNofy.remove()` method.
        """
        cn = CallNofy(text, dosk)
        self.screen.mount(cn)
        self.install_screen
        return cn
    
    async def aio_callnofy(
        self,
        text: str,
        dosk: Literal["bottom", "left", "right", "top"]="top"
    ) -> CallNofy:
        """Creating a notification.
        
        Args:
            text (str): The text of the notification.
            dosk (Literal[\"bottom\", \"left\", \"right\", \"top\"], optional): Regarding the screen. Defaults to "top".
        
        Returns:
            CallNofy: To delete the notification image, use the `CallNofy.remove()` method.
        """
        cn = CallNofy(text, dosk)
        await self.screen.mount(cn)
        return cn
    
    # ! Get Current Sound
    def gcs(self) -> Optional[CodecBase]:
        """Getting the currently selected sound.
        
        Returns:
            Optional[CodecBase]: The image of the codec in which the sound is wrapped.
        """
        return self.currect_sound
    
    async def aio_gcs(self) -> Optional[CodecBase]:
        """Getting the currently selected sound.
        
        Returns:
            Optional[CodecBase]: The image of the codec in which the sound is wrapped.
        """
        return self.currect_sound
    
    # ! Get Current Sound Status Text
    def get_sound_tstatus(self, sound: CodecBase) -> str:
        """Getting the audio status in text format in the language selected by the user.
        
        Args:
            sound (CodecBase): The image of the codeс in which the sound is wrapped.
        
        Returns:
            str: Audio status in text format in the language selected by the user.
        """
        if sound.playing:
            if sound.paused:
                return self.ll.get("sound.status.paused")
            else:
                return self.ll.get("sound.status.playing")
        return self.ll.get("sound.status.stopped")
    
    def get_sound_selected_label_text(self, sound: Optional[CodecBase]=None) -> str:
        """Generating a string for `self.music_selected_label`.
        
        Args:
            sound (Optional[CodecBase], optional): The image of the codeс in which the sound is wrapped. Defaults to None.
        
        Returns:
            str: String for `self.music_selected_label`.
        """
        if sound is None:
            sound = self.gcs()
        if sound is not None:
            return f"({self.get_sound_tstatus(sound)}): {get_sound_basename(sound)}"
        return self.ll.get("player.bar.sound.none")
    
    async def aio_get_sound_selected_label_text(self, sound: Optional[CodecBase]=None) -> str:
        """Generating a string for `self.music_selected_label`.
        
        Args:
            sound (Optional[CodecBase], optional): The image of the codeс in which the sound is wrapped. Defaults to None.
        
        Returns:
            str: String for `self.music_selected_label`.
        """
        if sound is None:
            sound = await self.aio_gcs()
        if sound is not None:
            return f"({self.get_sound_tstatus(sound)}): {get_sound_basename(sound)}"
        return self.ll.get("player.bar.sound.none")
    
    # ! Update Selected Label Text
    def update_select_label(self, sound: Optional[CodecBase]=None) -> None:
        """Updating the string in `self.music_selected_label`.
        
        Args:
            sound (Optional[CodecBase], optional): The image of the codeс in which the sound is wrapped. Defaults to None.
        """
        self.player_selected_label.update(self.get_sound_selected_label_text(sound))
    
    async def aio_update_select_label(self, sound: Optional[CodecBase]=None) -> None:
        """Updating the string in `self.music_selected_label`.
        
        Args:
            sound (Optional[CodecBase], optional): The image of the codeс in which the sound is wrapped. Defaults to None.
        """
        self.player_selected_label.update(await self.aio_get_sound_selected_label_text(sound))
    
    # ! Update Selected Image
    async def aio_update_select_image(self, sound: Optional[CodecBase]) -> None:
        """Forced image update.
        
        Args:
            sound (Optional[CodecBase]): The current sound.
        """
        image = None
        if sound is not None:
            if sound.icon_data is not None:
                image = image_from_bytes(sound.icon_data)
        await self.player_image.update_image(image)
    
    # ! Update Currect Sound
    async def aio_update_currect_sound(self) -> None:
        """Updating local variables of the current sound."""
        self.currect_sound = self.playlist_view.currect_sound
        self.currect_sound_index = self.playlist_view.currect_sound_index
        if self.currect_sound is not None:
            self.currect_sound.set_volume(self.currect_volume)
    
    # ! Switch Mode Button
    def gpms(
        self,
        modes: Tuple[str, str, str]=(
            ll.get("player.button.mode.play"),
            ll.get("player.button.mode.replay_sound"),
            ll.get("player.button.mode.replay_list")
        )
    ) -> str:
        return modes[self.playback_mode]
    
    def switch_playback_mode(self) -> None:
        if self.playback_mode == 2:
            self.playback_mode = 0
        else:
            self.playback_mode += 1
    
    # ! Callback Functions
    async def get_sound_seek(self) -> Tuple[str, Optional[float], Optional[float]]:
        if (sound:=await self.aio_gcs()) is not None:
            pos = sound.get_pos()
            minutes, seconds = round(pos // 60), round(pos % 60)
            return f"{minutes}:{str(seconds).rjust(2,'0')} | {str(round(sound.get_volume()*100)).rjust(3)}%", pos, sound.duration
        return "0:00 |   0%", None, None
    
    # ! Loop Functions
    async def playback_control_loop(self) -> None:
        while self.started:
            sound = await self.aio_gcs()
            if sound is not None:
                if self.last_playback_status is not None:
                    if self.playback_mode != 0:
                        status = await aio_check_status_code(sound)
                        if (self.last_playback_status == 1) and (status == 0):
                            if not self.block_playback_control:
                                self.info(f"The status of the current sound has changed to: {repr(status)}.")
                                if self.playback_mode == 1:
                                    self.currect_sound.play()
                                    await self.aio_update_select_label(sound)
                                    self.last_playback_status = 0
                                    self.info(f"Replay this sound: {repr(self.currect_sound)}.")
                                elif self.playback_mode == 2:
                                    self.block_select = True
                                    await self.playlist_view.aio_select_next_sound()
                                    await self.aio_update_currect_sound()
                                    if self.currect_sound is not None:
                                        self.currect_sound.play()
                                    await self.aio_update_select_label(self.currect_sound)
                                    await self.aio_update_select_image(self.currect_sound)
                                    self.last_playback_status = 0
                                    self.block_select = False
                                    self.info(f"Play next sound: {repr(self.currect_sound)}.")
            await asyncio.sleep(0.1)
    
    # ! Mounting Function
    def compose(self) -> ComposeResult:
        # * Other
        self.info("---")
        self.info(f"{__title__} [#60fdff]v{__version__}[/#60fdff] from {__author__} ({__email__})")
        self.info(f"Source          : {__url__}")
        self.info(f"Environment     : {repr(self.env)}")
        self.info(f"Codecs          : {repr(self.env['seaplayer']['codecs'])}")
        self.info(f"Config Path     : {repr(self.config.filepath)}")
        self.info(f"CSS Dirpath     : {repr(CSS_LOCALDIR)}")
        self.info(f"Assets Dirpath  : {repr(ASSETS_DIRPATH)}")
        self.info(f"Codecs Kwargs   : {repr(self.env['seaplayer']['codecs_kwargs'])}")
        self.info(f"Language Loader : {repr(self.ll)}")
        
        # * Play Screen
        self.player_box = Container(classes="player-box")
        self.player_box.border_title = self.ll.get("player")
        
        # * Image Object Init
        self.player_selected_label = Label(
            self.get_sound_selected_label_text(),
            classes="player-selected-label"
        )
        if self.config.image_update_method == "sync":
            self.image_type = StandartImageLabel
        elif self.config.image_update_method == "async":
            self.image_type = AsyncImageLabel
        else:
            raise RuntimeError("The configuration 'image_update_method' is incorrect.")
        
        self.player_image = self.image_type(
            Image.open(IMGPATH_IMAGE_NOT_FOUND),
            resample=RESAMPLING_SAFE[self.config.image_resample_method]
        )
        self.info(f"The picture from the media file is rendered using the {repr(self.config.image_update_method)} method.")
        
        # * Compositions Screen
        self.playlist_box = Container(classes="playlist-box")
        self.playlist_box.border_title = self.ll.get("playlist")
        self.playlist_view = PlayListView(classes="playlist-view")
        
        self.playlist_add_sound_input = Input(
            classes="playlist-add-sound-input", id="addsoundinput",
            placeholder=self.ll.get("playlist.input.placeholder")
        )
        self.player_button_mode_switch = Button(
            self.gpms(),
            id="switch-playback-mode",
            variant="primary",
            classes="button-sound-control"
        )
        
        # * Adding
        yield Header()
        with self.player_box:
            with Vertical():
                with Container(classes="player-visual-panel"):
                    yield self.player_image
                with Container(classes="player-contol-panel"):
                    yield self.player_selected_label
                    yield IndeterminateProgress(getfunc=self.get_sound_seek)
                    with Horizontal(classes="box-buttons-sound-control"):
                        yield Button(
                            self.ll.get("player.button.pause"),
                            id="button-pause",
                            variant="success",
                            classes="button-sound-control"
                        )
                        yield Static(classes="pass-one-width")
                        yield Button(
                            self.ll.get("player.button.psu"),
                            id="button-play-stop",
                            variant="warning",
                            classes="button-sound-control"
                        )
                        yield Static(classes="pass-one-width")
                        yield self.player_button_mode_switch
        with self.playlist_box:
            yield self.playlist_view
            yield self.playlist_add_sound_input
        yield self.log_menu
        yield Footer()
        self.pcw = self.run_worker(
            self.playback_control_loop,
            name="Playback Control Loop",
            group="seaplayer-main",
            description="Control of playback modes and status updates.",
            thread=True
        )
        self.info("---")
    
    # ! Currect Sound Controls
    async def currect_sound_stop(self, sound: Optional[CodecBase]=None):
        """Stops playback of the currently selected sound.
        
        Args:
            sound (Optional[CodecBase], optional): Сurrently selected sound. Defaults to None.
        """
        if sound is None:
            sound = await self.aio_gcs()
        if sound is not None:
            self.last_playback_status = 0
            sound.stop()
    
    async def currect_sound_play(self, sound: Optional[CodecBase]=None):
        """Plays playback of the currently selected sound.
        
        Args:
            sound (Optional[CodecBase], optional): Сurrently selected sound. Defaults to None.
        """
        if sound is None:
            sound = await self.aio_gcs()
        if sound is not None:
            self.last_playback_status = 1
            sound.play()
    
    async def currect_sound_pause(self, sound: Optional[CodecBase]=None):
        """Pauses the currently selected sound.
        
        Args:
            sound (Optional[CodecBase], optional): Сurrently selected sound. Defaults to None.
        """
        if sound is None:
            sound = await self.aio_gcs()
        if sound is not None:
            self.last_playback_status = 3
            sound.pause()
    
    async def currect_sound_unpause(self, sound: Optional[CodecBase]=None):
        """Unpauses the currently selected sound.
        
        Args:
            sound (Optional[CodecBase], optional): Сurrently selected sound. Defaults to None.
        """
        if sound is None:
            sound = await self.aio_gcs()
        if sound is not None:
            self.last_playback_status = 1
            sound.unpause()
    
    # ! Sound Controls
    async def adding_sounds_loader(self, handlered_values: List[str]) -> None:
        added_oks = 0
        loading_nofy = await self.aio_callnofy(
            self.ll.get("nofys.sound.found").format(count=len(handlered_values))
        )
        self.env['seaplayer']['codecs'].sort(key=lambda x: x.codec_priority)
        codec: CodecBase
        async for value in aiter(handlered_values):
            sound = None
            async for codec in aiter(self.env['seaplayer']['codecs']):
                self.info(f"Attempt to load via {repr(codec)}")
                try:
                    if hasattr(codec, "aio_is_this_codec"):
                        this_codec = await codec.aio_is_this_codec(value)
                    else:
                        this_codec = codec.is_this_codec(value)
                    if this_codec:
                        if hasattr(codec, "__aio_init__"):
                            try:
                                sound: CodecBase = await codec.__aio_init__(value, **self.env['seaplayer']['codecs_kwargs'])
                            except Exception as e:
                                sound = None
                                raise e
                        else:
                            try:
                                sound: CodecBase = codec(value, **self.env['seaplayer']['codecs_kwargs'])
                            except Exception as e:
                                sound = None
                                raise e
                        if sound is not None:
                            if not await self.playlist_view.aio_exist_sound(sound):
                                await self.playlist_view.aio_add_sound(sound)
                                self.info(f"Song added: {repr(sound)}")
                                added_oks += 1
                                break
                except FileNotFoundError:
                    self.error(f"The file does not exist or is a directory: {repr(value)}")
                    break
                except OSError:
                    pass
                except Exception as e:
                    self.exception(e)
            if sound is None:
                self.error(f"The sound could not be loaded: {repr(value)}")
        await loading_nofy.remove()
        self.info(f"Added [cyan]{added_oks}[/cyan] songs!")
        await self.aio_nofy(self.ll.get("nofys.sound.added").format(count=added_oks))
    
    # ! Worker Functions
    async def pl_select(self) -> None:
        if self.playlist_view.currect_sound_index != self.currect_sound_index:
            
            if self.currect_sound is not None:
                self.currect_sound.stop()
            await self.aio_update_currect_sound()
            await self.aio_update_select_label(self.currect_sound)
            await self.aio_update_select_image(self.currect_sound)
            self.last_playback_status = await aio_check_status_code(self.currect_sound)
        self.block_playback_control = False
    
    # ! Playlist Actions
    @on(ListView.Selected, ".playlist-view")
    async def pl_select_worker(self) -> None:
        if not self.block_select:
            self.block_playback_control = True
            self.run_worker(
                self.pl_select,
                name="Playlist Select",
                group="seaplayer-temp",
                description="Update: status, images and so on."
            )
        else:
            self.info("The sound selection is blocked.")
    
    # ! Input Actions
    @on(Input.Submitted, "#addsoundinput")
    async def input_add_sound(self) -> None:
        value = self.playlist_add_sound_input.value
        self.playlist_add_sound_input.value = ""
        if len(value.replace(" ", "")) > 0:
            self.run_worker(
                awrap(self.adding_sounds_handler, value),
                name="Adding Sounds Handler",
                group="seaplayer-temp"
            )
    
    # ! Button Actions
    @on(Button.Pressed, "#switch-playback-mode")
    async def on_button_pressed(self) -> None:
        self.switch_playback_mode()
        self.player_button_mode_switch.label = self.gpms()
    
    @on(Button.Pressed, "#button-pause")
    async def bp_pause_unpause(self) -> None:
        if (sound:=await self.aio_gcs()) is not None:
            if sound.playing:
                await self.currect_sound_pause(sound)
            await self.aio_update_select_label(sound)
    
    @on(Button.Pressed, "#button-play-stop")
    async def bp_play_stop(self) -> None:
        if (sound:=await self.aio_gcs()) is not None:
            if sound.playing:
                if sound.paused:
                    await self.currect_sound_unpause(sound)
                else:
                    await self.currect_sound_stop(sound)
            else:
                await self.currect_sound_play(sound)
            await self.aio_update_select_label(sound)
    
    # ! Input Submits
    async def adding_sounds_handler(self, value: str) -> None:
        handlered_values = []
        try: handlered_values = glob.glob(value, recursive=self.config.recursive_search)
        except: pass
        if ENABLE_PLUGIN_SYSTEM:
            for vhr in self.plugin_loader.value_handlers:
                handlered_values += vhr(value)
        self.info(f"Submit 'plus_sound' values: {repr(handlered_values)}")
        if len(handlered_values) > 0:
            self.run_worker(
                awrap(self.adding_sounds_loader, handlered_values),
                name="Adding Sounds Loader",
                group="seaplayer-temp",
                description="The process of adding sounds to a playlist."
            )
    
    # ! Keys Actions
    async def action_plus_rewind(self):
        if (sound:=await self.aio_gcs()) is not None:
            sound.set_pos(sound.get_pos()+self.config.rewind_count_seconds)
    
    async def action_minus_rewind(self):
        if (sound:=await self.aio_gcs()) is not None:
            sound.set_pos(sound.get_pos()-self.config.rewind_count_seconds)
    
    async def action_plus_volume(self) -> None:
        if (sound:=await self.aio_gcs()) is not None:
            if (vol:=round(sound.get_volume()+self.config.volume_change_percent, 2)) <= self.config.max_volume_percent:
                self.currect_volume = vol
                sound.set_volume(vol)
    
    async def action_minus_volume(self) -> None:
        if (sound:=await self.aio_gcs()) is not None:
            if (vol:=round(sound.get_volume()-self.config.volume_change_percent, 2)) >= 0:
                self.currect_volume = vol
                sound.set_volume(vol)
    
    async def action_screenshot(self) -> None:
        path = self.save_screenshot(path=LOCALDIR)
        self.info(f"Screenshot saved to: {repr(path)}")
        await self.aio_nofy(self.ll.get("nofys.screenshot.saved").format(path=repr(path)))
    
    async def action_quit(self) -> None:
        """The function called by our when the SeaPlayer stops working."""
        self.started = False
        if ENABLE_PLUGIN_SYSTEM:
            await self.plugin_loader.on_quit()
        if (sound:=await self.aio_gcs()) is not None:
            sound.unpause()
            sound.stop()
        return await super().action_quit()
    
    # ! On Functions
    async def on_compose(self) -> None:
        if ENABLE_PLUGIN_SYSTEM:
            self.run_worker(
                self.plugin_loader.on_compose,
                name="On Compose",
                group="pluginloader",
                description="<method PluginLoader.on_compose>"
            )
    
    def on_ready(self, *args, **kwargs) -> None:
        """A function called when the SeaPlayer is completely confused."""
        if ENABLE_PLUGIN_SYSTEM:
            self.run_worker(
                self.plugin_loader.on_ready,
                name="On Ready",
                group="pluginloader",
                description="<method PluginLoader.on_ready>"
            )
    
    # ! Other
    def run(self, *args, **kwargs):
        if ENABLE_PLUGIN_SYSTEM:
            self.plugin_loader.on_run()
        super().run(*args, **kwargs)
