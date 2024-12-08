from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer
from textual.binding import BindingType, Binding, _Bindings
# > Typing
try:
    from sounddevice import query_devices, query_hostapis
    INIT_SOUNDDEVICE = True
except:
    INIT_SOUNDDEVICE = False
from typing import Optional, Literal, Union, Tuple, Dict, List, Any
# > Local Imports
from ..languages import LanguageLoader
from ..types import Converter
from ..modules.colorizer import richefication
from ..objects import (
    Nofy,
    Rheostat,
    InputField,
    DataOptionList, DataOption,
    DataRadioSet, DataRadioButton,
    ConfigurateList, ConfigurateListItem
)

# ! Vars
conv = Converter()

# ! Functions
if INIT_SOUNDDEVICE:
    def generate_devices_options(currect: Optional[int]=None):
        hosts: List[Dict[str, Any]] = [_1 for _1 in query_hostapis()]
        devices: List[Dict[str, Any]] = [_2 for _2 in query_devices()]
        devices_options: List[DataOption] = []
        devices_options.append(DataOption("([cyan]*[/cyan]) [yellow]Auto[/yellow]", device_index=None))
        
        for device in devices:
            if device["max_output_channels"] > 0:
                try:
                    format_data = dict(
                        device_name=device["name"], 
                        device_index=device["index"],
                        hostapi_index=device["hostapi"],
                        hostapi_name=hosts[device["hostapi"]]["name"]
                    )
                    devices_options.append(
                        DataOption(
                            "([cyan]{device_index}[/cyan]) [yellow]{device_name}[/yellow] \[[green]{hostapi_name}[/green]]".format(**format_data),
                            device_index=device["index"]
                        )
                    )
                except:
                    pass
        for d in devices_options:
            if d.data["device_index"] == currect:
                d.selected = True
        return devices_options

# ! Main Class
class Configurate(Screen):
    """This Configurate Menu screen."""
    # ! Propertyes
    @property
    def ll(self) -> LanguageLoader:
        return self.app.ll
    
    @property
    def bindings(self) -> List[Binding]:
        return self._bindings.shown_keys
    @bindings.setter
    def bindings(self, value: List[BindingType]) -> None:
        self.BINDINGS = value
        self._bindings = _Bindings(value)
    
    # ! Nofy Functions
    def nofy(
        self,
        text: str,
        life_time: float=3,
        dosk: Literal["bottom", "left", "right", "top"]="top"
    ) -> None:
        self.screen.mount(Nofy(text, life_time, dosk))
    
    async def aio_nofy(
        self,
        text: str,
        life_time: float=3,
        dosk: Literal["bottom", "left", "right", "top"]="top"
    ) -> None:
        await self.screen.mount(Nofy(text, life_time, dosk))
    
    # ! Update Placeholder from InputField
    def _upfif(self, attr_name: str) -> str:
        return self.ll.get("words.currect")+": " + str(eval(f"self.{attr_name}"))
    
    def gupfif(self, attr_name: str):
        return lambda: self._upfif(attr_name)
    
    # ! Update App Vars
    def sattr(self, attr_name: str, value: Any) -> None:
        exec(f"self.{attr_name}=value")
    
    def gattr(self, attr_name: str) -> Any:
        return eval(f"self.{attr_name}")
    
    async def _auac(self, attr_name: str, input: InputField, value: str) -> None:
        self.sattr(attr_name, value)
        self.app.update_bindings()
        await self.aio_nofy("Saved!")
    
    def _caa(self, attr_name: str, value: str) -> None:
        self.sattr(attr_name, value)
        self.app.update_bindings()
        self.nofy("Saved!")
    
    if INIT_SOUNDDEVICE:
        def gucsdi(self):
            async def n_ucsdi(option: DataOption) -> None:
                self.app.config.output_sound_device_id = option.data.get("device_index", None)
                await self.aio_nofy("Saved!")
            return n_ucsdi
    
    def guac(self, attr_name: str):
        async def an_uac(input: InputField, value: str) -> None:
            await self._auac(attr_name, input, value)
        return an_uac
    
    # ! Configurator Generators
    def create_configurator_type(
        self,
        attr_name: str,
        group: str="Option",
        title: str="",
        desc: str="",
        _type: type=str,
        type_alias: type=str,
        restart_required: bool=True
    ) -> ConfigurateListItem:
        return ConfigurateListItem(
            InputField(
                conv=conv.gen_aio_conv(_type),
                submit=self.guac(attr_name),
                update_placeholder=self.gupfif(attr_name)
            ),
            title="[red]{"+group+"}[/red]: "+f"{title} ({richefication(type_alias)})",
            desc=desc+(f" [red]({self.ll.get('words.restart_required')})[/red]" if restart_required else ""),
            height=5
        )
    
    def create_configurator_keys(
        self,
        attr_name: str,
        title: str="",
        desc: str="",
        restart_required: bool=True
    ) -> ConfigurateListItem:
        return ConfigurateListItem(
            InputField(
                submit=self.guac(attr_name),
                update_placeholder=self.gupfif(attr_name)
            ),
            title="[red]{"+self.ll.get("configurate.keys")+"}[/red]: "+f"{title} ({richefication(str)})",
            desc=desc+(f" [red]({self.ll.get('words.restart_required')})[/red]" if restart_required else ""),
            height=5
        )
    
    def create_configurator_literal(
        self,
        attr_name: str,
        values: List[Union[Any, Tuple[Any, str]]],
        group: str="Option",
        title: str="",
        desc: str="",
        restart_required: bool=True
    ) -> ConfigurateListItem:
        on_changed_method = lambda v: self._caa(attr_name, v)
        default_value = [v[0] if isinstance(v, tuple) else v for v in values].index(self.gattr(attr_name))
        buttons = []
        for idx, d in enumerate(values):
            drb = \
                DataRadioButton(d[0], idx==default_value, d[1]) \
            if isinstance(d, tuple) else \
                DataRadioButton(d, idx==default_value)
            buttons.append(drb)
        return ConfigurateListItem(
            DataRadioSet(on_changed_method, *buttons),
            title="[red]{"+group+"}[/red]: "+title,
            desc=desc+(f" [red]({self.ll.get('words.restart_required')})[/red]" if restart_required else ""),
            height=len(values)+4
        )
    
    def create_configurator_integer(
        self,
        attr_name: str,
        advance_value: int=1,
        min_value: int=0,
        max_value: int=100,
        mark: str="",
        group: str="Option",
        title: str="",
        desc: str="",
        restart_required: bool=True
    ):
        return ConfigurateListItem(
            Rheostat(lambda value: self.sattr(attr_name, value), self.gattr(attr_name), advance_value, min_value, max_value, mark),
            title="[red]{"+group+"}[/red]: "+title,
            desc=desc+(f" [red]({self.ll.get('words.restart_required')})[/red]" if restart_required else ""),
            height=4
        )

    def create_configurator_percent(
        self,
        attr_name: str,
        advance_value: int=1,
        min_value: int=0,
        max_value: int=100,
        group: str="Option",
        title: str="",
        desc: str="",
        restart_required: bool=True
    ):
        return ConfigurateListItem(
            Rheostat(lambda value: self.sattr(attr_name, value/100), int(self.gattr(attr_name)*100), advance_value, min_value, max_value, "%"),
            title="[red]{"+group+"}[/red]: "+title,
            desc=desc+(f" [red]({self.ll.get('words.restart_required')})[/red]" if restart_required else ""),
            height=4
        )
    
    def create_configurator_language(self) -> ConfigurateListItem:
        languages = []
        for lang in self.ll.langs:
            if lang.author_url is not None:
                text = f"{lang.title} ({lang.words['from']} [link={lang.author_url}]{lang.author}[/link])"
            else:
                text = f"{lang.title} ({lang.words['from']} {lang.author})"
            languages.append((lang.mark, text))
        return self.create_configurator_literal(
            "app.config.lang",
            languages,
            self.ll.get("configurate.main"),
            self.ll.get("configurate.main.lang"),
            self.ll.get("configurate.main.lang.desc")
        )
    
    if INIT_SOUNDDEVICE:
        def create_configurator_sound_devices(self):
            dos = generate_devices_options(self.app.config.output_sound_device_id)
            options_list = DataOptionList(*dos, group="SoundDevicesSelect", after_selected=self.gucsdi())
            return ConfigurateListItem(
                options_list,
                title="[red]{"+self.ll.get("configurate.sound")+"}[/]: "+self.ll.get("configurate.sound.output_device"),
                desc=self.ll.get("configurate.sound.output_device.desc"),
                height=len(dos)+4
            )
    
    # ! Configurate Main Functions
    def compose(self) -> ComposeResult:
        self.bindings = [Binding("escape", "app.pop_screen", self.ll.get("configurate.footer.back"))]
        # ? Compose
        self.congigurate_list = ConfigurateList()
        self.congigurate_list.border_title = self.ll.get("configurate")
        yield Header()
        with self.congigurate_list:
            yield self.create_configurator_language()
            yield self.create_configurator_type(
                "app.config.sound_font_path",
                self.ll.get("configurate.sound"),
                self.ll.get("configurate.sound.font_path"),
                self.ll.get("configurate.sound.font_path.desc"),
                conv.optional(conv.filepath), Optional[str], False
            )
            if INIT_SOUNDDEVICE:
                yield self.create_configurator_sound_devices()
            yield self.create_configurator_literal(
                "app.config.image_update_method",
                [
                    ("sync", self.ll.get("configurate.image.update_method.sync")),
                    ("async", self.ll.get("configurate.image.update_method.async"))
                ],
                self.ll.get("configurate.image"),
                self.ll.get("configurate.image.update_method"),
                self.ll.get("configurate.image.update_method.desc")
            )
            yield self.create_configurator_literal(
                "app.config.image_resample_method",
                [
                    ("nearest", self.ll.get("configurate.image.resample_method.nearest")),
                    ("bilinear", self.ll.get("configurate.image.resample_method.bilinear")),
                    ("bicubic", self.ll.get("configurate.image.resample_method.bicubic")),
                    ("lanczos", self.ll.get("configurate.image.resample_method.lanczos")),
                    ("hamming", self.ll.get("configurate.image.resample_method.hamming")),
                    ("box", self.ll.get("configurate.image.resample_method.box")),
                ],
                self.ll.get("configurate.image"),
                self.ll.get("configurate.image.resample_method"),
                self.ll.get("configurate.image.resample_method.desc")
            )
            yield self.create_configurator_percent(
                "app.config.volume_change_percent",
                1, 1, 10,
                self.ll.get("configurate.playback"),
                self.ll.get("configurate.playback.volume_change_percent"),
                self.ll.get("configurate.playback.volume_change_percent.desc"),
                False
            )
            yield self.create_configurator_integer(
                "app.config.rewind_count_seconds",
                1, 1, 30, f" {self.ll.get('words.second.char')}",
                self.ll.get("configurate.playback"),
                self.ll.get("configurate.playback.rewind_count_seconds"),
                self.ll.get("configurate.playback.rewind_count_seconds.desc"),
                False
            )
            yield self.create_configurator_percent(
                "app.config.max_volume_percent",
                10, 10, 300,
                self.ll.get("configurate.playback"),
                self.ll.get("configurate.playback.max_volume_percent"),
                self.ll.get("configurate.playback.max_volume_percent.desc"),
                False
            )
            yield self.create_configurator_literal(
                "app.config.recursive_search",
                [
                    (True, self.ll.get("words.on")),
                    (False, self.ll.get("words.off"))
                ],
                self.ll.get("configurate.playlist"),
                self.ll.get("configurate.playlist.recursive_search"),
                self.ll.get("configurate.playlist.recursive_search.desc"),
                False
            )
            yield self.create_configurator_literal(
                "app.config.logging",
                [
                    (True, self.ll.get("words.on")),
                    (False, self.ll.get("words.off"))
                ],
                self.ll.get("configurate.debug"),
                self.ll.get("configurate.debug.logging"),
                self.ll.get("configurate.debug.logging.desc"),
                False
            )
            # ! Keys
            yield self.create_configurator_keys(
                "app.config.key_quit",
                self.ll.get("configurate.keys.quit"),
                self.ll.get("configurate.keys.quit.desc"),
                False
            )
            yield self.create_configurator_keys(
                "app.config.key_rewind_forward",
                self.ll.get("configurate.keys.rewind_forward"),
                self.ll.get("configurate.keys.rewind_forward.desc"),
                False
            )
            yield self.create_configurator_keys(
                "app.config.key_rewind_back",
                self.ll.get("configurate.keys.rewind_back"),
                self.ll.get("configurate.keys.rewind_back.desc"),
                False
            )
            yield self.create_configurator_keys(
                "app.config.key_volume_up",
                self.ll.get("configurate.keys.volume_plus"),
                self.ll.get("configurate.keys.volume_plus.desc"),
                False
            )
            yield self.create_configurator_keys(
                "app.config.key_volume_down",
                self.ll.get("configurate.keys.volume_minus"),
                self.ll.get("configurate.keys.volume_minus.desc"),
                False
            )
        yield Footer()
