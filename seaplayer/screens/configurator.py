import sounddevice as sd
from enum import Flag, auto
from PIL.Image import Resampling
# > Textual
from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.binding import Binding
from textual.widgets import Header, Footer, OptionList, RadioSet
from textual.containers import VerticalScroll, Container
# > Local Imports
from seaplayer.units import config, ll, logger
from seaplayer.config import Config
from seaplayer.languages import LanguageLoader
from seaplayer.objects.image import RenderMode
from seaplayer.objects.optionitem import OptionItem
from seaplayer.objects.radioitem import RadioItem
# > Typing
from typing_extensions import (
    Any, Tuple, List,
    Iterator, Iterable, Mapping, TypedDict,
    TypeAlias
)

# ! Types

class ConfigurateState(Flag):
    LANGUAGE = auto()
    DEVICE_ID = auto()
    IMAGE_RESAMPLING = auto()
    IMAGE_RENDER_MODE = auto()

# ! Types Alias

class DeviceInfo(TypedDict):
    name: str
    index: int
    hostapi: int
    max_input_channels: int
    max_output_channels: int
    default_low_input_latency: float
    default_low_output_latency: float
    default_high_input_latency: float
    default_high_output_latency: float
    default_samplerate: float

class HostAPIInfo(TypedDict):
    name: str
    devices: List[int]
    default_input_device: int
    default_output_device: int

DevicesInfo: TypeAlias = Iterable[DeviceInfo]
HostAPIsInfo: TypeAlias = Tuple[HostAPIInfo]

# ! Methods

def _rr(_: bool):
    if _:
        return ' [red]\\[%s][/red]' % ll.get('words.restart_required')
    return ''

# ! Spetific Methods

def query_sounddevices() -> Iterator[Tuple[int, str, str]]:
    hosts: HostAPIsInfo = sd.query_hostapis()
    devices: DevicesInfo = sd.query_devices()
    for device in filter(lambda i: i.get('max_output_channels', 0) > 0, devices):
        yield device['index'], device['name'], hosts[device['hostapi']]['name']

# ! Main Configration Screen

class ConfigurationScreen(Screen):
    BINDINGS = [
        Binding('escape', 'app.pop_screen', ll.get('configurate.footer.back'), priority=True),
    ]
    SUB_TITLE = ll.get('configurate')
    CSS = """
    VerticalScroll.configurations-container {
        border: solid cyan;
        border-title-align: left;
    }
    Container.configuration-item-container {
        border: solid cornflowerblue;
        border-title-align: left;
        border-subtitle-align: right;
        border-title-color: white;
        border-subtitle-color: gray;
    }
    """
    
    # ^ Variables
    
    configurate_state = ConfigurateState(0)
    
    # ^ Create Configurate Parameters Methods
    
    def create_configurate_literal(self,
        config: Config,
        ll: LanguageLoader,
        id: str,
        key_name: str,
        key_desc: str,
        variants: Iterable[Tuple[str, Any]] | Mapping[str, Any],
        current_value: Any,
        restart_request: bool=True
    ) -> ComposeResult:
        yield from []
        variants = {ll.get(key): data for key, data in dict(variants).items()}
        with Container(classes='configuration-item-container') as container:
            container.border_title = ll.get(key_name)
            container.border_subtitle = ll.get(key_desc) + _rr(restart_request)
            length = 0
            with RadioSet(id=id):
                for text, data in variants.items():
                    value = (current_value == data)
                    length += 1
                    yield RadioItem(text, value, data=data)
            container.styles.height = length + 4
    
    def create_configurate_options(self,
        config: Config,
        ll: LanguageLoader,
        id: str,
        key_name: str,
        key_desc: str,
        variants: Iterable[Tuple[str, Any]] | Mapping[str, Any],
        current_value: Any,
        restart_request: bool=True
    ) -> ComposeResult:
        yield from []
        variants = dict(variants)
        with Container(classes='configuration-item-container') as container:
            container.border_title = ll.get(key_name)
            container.border_subtitle = ll.get(key_desc) + _rr(restart_request)
            options, selected_index = [], 0
            for index, variant in enumerate(variants.items()):
                text, data = variant
                options.append(OptionItem(text, data))
                if data == current_value:
                    selected_index = index
            option_list = OptionList(*options, id=id)
            container.styles.height = len(options)+4
            option_list.highlighted = selected_index
            yield option_list
    
    # ^ Spetific Configurate Parameters Methods
    
    def create_configurate_language(self, config: Config, ll: LanguageLoader) -> ComposeResult:
        yield from []
        if ConfigurateState.LANGUAGE not in self.configurate_state:
            variants = {}
            for lang in ll.langs:
                if lang.author_url is not None:
                    key = f"{lang.title} ({lang.words['from']} [link={lang.author_url}]{lang.author}[/link])"
                else:
                    key = f"{lang.title} ({lang.words['from']} {lang.author})"
                variants[key] = lang.mark
            yield from self.create_configurate_options(
                config, ll, 'configurate-language-optionlist',
                'configurate.main.lang',
                'configurate.main.lang.desc',
                variants, config.main.language
            )
            self.configurate_state |= ConfigurateState.LANGUAGE
    
    def create_configurate_device_id(self, config: Config, ll: LanguageLoader) -> ComposeResult:
        yield from []
        if ConfigurateState.DEVICE_ID not in self.configurate_state:
            variants = {
                "([#5f87ff]*[/#5f87ff]) [yellow]Auto[/yellow]": None,
                **{
                    f"([#5f87ff]{device_id}[/#5f87ff]) [yellow]{device_name}[/yellow] \\[[green]{hostapi_name}[/green]]": device_id \
                        for device_id, device_name, hostapi_name in query_sounddevices()
                }
            }
            yield from self.create_configurate_options(
                config, ll, 'configurate-device-id',
                'configurate.sound.output_device',
                'configurate.sound.output_device.desc',
                variants,
                config.main.device_id
            )
            self.configurate_state |= ConfigurateState.DEVICE_ID
    
    def create_configurate_image_resample_method(self, config: Config, ll: LanguageLoader) -> ComposeResult:
        yield from []
        if ConfigurateState.IMAGE_RESAMPLING not in self.configurate_state:
            yield from self.create_configurate_literal(
                config, ll, 'configurate-image-resample-radioset',
                'configurate.image.resample_method',
                'configurate.image.resample_method.desc',
                {
                    'configurate.image.resample_method.nearest': Resampling.NEAREST,
                    'configurate.image.resample_method.lanczos': Resampling.LANCZOS,
                    'configurate.image.resample_method.bilinear': Resampling.BILINEAR,
                    'configurate.image.resample_method.bicubic': Resampling.BICUBIC,
                    'configurate.image.resample_method.box': Resampling.BOX,
                    'configurate.image.resample_method.hamming': Resampling.HAMMING,
                },
                config.image.resample
            )
            self.configurate_state |= ConfigurateState.IMAGE_RESAMPLING
    
    def create_configurate_image_render_mode(self, config: Config, ll: LanguageLoader) -> ComposeResult:
        yield from []
        if ConfigurateState.IMAGE_RENDER_MODE not in self.configurate_state:
            yield from self.create_configurate_literal(
                config, ll, 'configurate-image-render-mode-radioset',
                'configurate.image.render_mode',
                'configurate.image.render_mode.desc',
                {
                    'configurate.image.render_mode.none': RenderMode.NONE,
                    'configurate.image.render_mode.full': RenderMode.FULL,
                    'configurate.image.render_mode.half': RenderMode.HALF,
                },
                config.image.render_mode
            )
            self.configurate_state |= ConfigurateState.IMAGE_RENDER_MODE
    
    # ^ Callbacks
    
    @on(OptionList.OptionSelected, '#configurate-language-optionlist')
    async def action_language_selected(self, event: OptionList.OptionSelected) -> None:
        if ConfigurateState.LANGUAGE in self.configurate_state:
            item: OptionItem[str] = event.option
            config.main.language = item.data
            config.refresh()
            self.notify(ll.get('nofys.config.saved'), timeout=1.0)
            logger.trace(f'Updated [yellow]config.main.language[/yellow]={config.main.language!r}')
    
    @on(OptionList.OptionSelected, '#configurate-device-id')
    async def action_device_id_selected(self, event: OptionList.OptionSelected) -> None:
        if ConfigurateState.DEVICE_ID in self.configurate_state:
            item: OptionItem[int | None] = event.option
            config.main.device_id = item.data
            config.refresh()
            self.notify(ll.get('nofys.config.saved'), timeout=1.0)
            logger.trace(f'Updated [yellow]config.main.device_id[/yellow]={config.main.device_id!r}')
    
    @on(RadioSet.Changed, '#configurate-image-resample-radioset')
    async def action_image_resample_changed(self, event: RadioSet.Changed) -> None:
        if ConfigurateState.IMAGE_RESAMPLING in self.configurate_state:
            item: RadioItem[Resampling] = event.radio_set.children[event.index]
            config.image.resample = item.data
            config.refresh()
            self.notify(ll.get('nofys.config.saved'), timeout=1.0)
            logger.trace(f'Updated [yellow]config.image.resample[/yellow]={config.image.resample!r}')
    
    @on(RadioSet.Changed, '#configurate-image-render-mode-radioset')
    async def action_image_render_mode_changed(self, event: RadioSet.Changed) -> None:
        if ConfigurateState.IMAGE_RENDER_MODE in self.configurate_state:
            item: RadioItem[RenderMode] = event.radio_set.children[event.index]
            config.image.render_mode = item.data
            config.refresh()
            self.notify(ll.get('nofys.config.saved'), timeout=1.0)
            logger.trace(f'Updated [yellow]config.image.render_mode[/yellow]={config.image.render_mode!r}')
    
    # ^ Compose
    
    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(classes='configurations-container') as configurations_container:
            yield from self.create_configurate_language(config, ll)
            yield from self.create_configurate_device_id(config, ll)
            yield from self.create_configurate_image_resample_method(config, ll)
            yield from self.create_configurate_image_render_mode(config, ll)
        configurations_container.border_title = ll.get('configurate')
        yield Footer()