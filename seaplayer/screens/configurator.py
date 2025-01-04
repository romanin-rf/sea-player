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
from seaplayer.functions import invert_items, item_by_attr
# > Local Imports (Objects)
from seaplayer.objects.image import RenderMode
from seaplayer.objects.optionitem import OptionItem
from seaplayer.objects.radioitem import RadioItem
from seaplayer.objects.log import LEVEL_NAMES, TextualLogLevel
# > Local Imports (Configurator)
from seaplayer.screens.configurator_units import ConfigurateState, _rr, query_sounddevices
# > Typing
from typing_extensions import (
    Any, Tuple,
    Literal,
    Iterable, Mapping,
)

# ! Constants

_OPTION_SELECTED_PREFIX = '[bold green]>[/bold green] '

# ! Main Configration Screen

class ConfigurationScreen(Screen):
    BINDINGS = [
        Binding('escape', 'app.pop_screen', ll.get('configurate.footer.back'), priority=True),
    ]
    SUB_TITLE = BINDING_GROUP_TITLE = ll.get('configurate')
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
        restart_request: bool=True,
        *,
        variants_key_format: Literal['lang', 'text']='lang'
    ) -> ComposeResult:
        yield from []
        match variants_key_format:
            case 'lang':
                variants = {ll.get(key): data for key, data in dict(variants).items()}
            case 'text':
                variants = dict(variants)
            case _:
                raise ValueError(f"Invalid {_}")
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
        restart_request: bool=True,
        *,
        variants_key_format: Literal['lang', 'text']='text'
    ) -> ComposeResult:
        yield from []
        match variants_key_format:
            case 'lang':
                variants = {ll.get(key): data for key, data in dict(variants).items()}
            case 'text':
                variants = dict(variants)
            case _:
                raise ValueError(f"Invalid {_}")
        with Container(classes='configuration-item-container') as container:
            container.border_title = ll.get(key_name)
            container.border_subtitle = ll.get(key_desc) + _rr(restart_request)
            options, selected_index = [], 0
            for index, variant in enumerate(variants.items()):
                text, data = variant
                item = OptionItem(text, data)
                if data == current_value:
                    selected_index = index
                    item._prompt = _OPTION_SELECTED_PREFIX + item._prompt
                options.append(item)
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
    
    def create_configurate_log_level(self, config: Config, ll: LanguageLoader) -> ComposeResult:
        yield from []
        if ConfigurateState.LOG_LEVEL not in self.configurate_state:
            variants = invert_items(LEVEL_NAMES)
            yield from self.create_configurate_literal(
                config, ll, 'configurate-log-level-radioset',
                'configurate.logging.log_level',
                'configurate.logging.log_level.desc',
                variants,
                config.main.log_level,
                variants_key_format='text'
            )
            self.configurate_state |= ConfigurateState.LOG_LEVEL
    
    # ^ Spetific Methods
    
    def _selget_option(self, event: OptionList.OptionSelected, data: Any):
        last_item: OptionItem = item_by_attr(event.option_list._contents, 'data', data)
        item: OptionItem = event.option
        last_item._prompt = last_item._prompt[len(_OPTION_SELECTED_PREFIX):]
        item._prompt = _OPTION_SELECTED_PREFIX + event.option._prompt
        event.option_list._refresh_lines()
        return item
    
    # ^ Callbacks
    
    @on(OptionList.OptionSelected, '#configurate-language-optionlist')
    async def action_language_selected(self, event: OptionList.OptionSelected) -> None:
        if ConfigurateState.LANGUAGE in self.configurate_state:
            item: OptionItem[str] = self._selget_option(event, config.main.language)
            config.main.language = item.data
            config.refresh()
            self.notify(ll.get('nofys.config.saved'), timeout=1.0)
            logger.trace(f'Updated [yellow]config.main.language[/yellow]={config.main.language!r}')
    
    @on(OptionList.OptionSelected, '#configurate-device-id')
    async def action_device_id_selected(self, event: OptionList.OptionSelected) -> None:
        if ConfigurateState.DEVICE_ID in self.configurate_state:
            item: OptionItem[int | None] = self._selget_option(event, config.main.device_id)
            config.main.device_id = item.data
            config.refresh()
            self.notify(ll.get('nofys.config.saved'), timeout=1.0)
            logger.trace(f'Updated [yellow]config.main.device_id[/yellow]={config.main.device_id!r}')
    
    @on(RadioSet.Changed, '#configurate-image-resample-radioset')
    async def action_image_resample_changed(self, event: RadioSet.Changed) -> None:
        if ConfigurateState.IMAGE_RESAMPLING in self.configurate_state:
            item: RadioItem[Resampling] = event.radio_set.children[event.index]
            event.radio_set._selected = event.index
            config.image.resample = item.data
            config.refresh()
            self.notify(ll.get('nofys.config.saved'), timeout=1.0)
            logger.trace(f'Updated [yellow]config.image.resample[/yellow]={config.image.resample!r}')
    
    @on(RadioSet.Changed, '#configurate-image-render-mode-radioset')
    async def action_image_render_mode_changed(self, event: RadioSet.Changed) -> None:
        if ConfigurateState.IMAGE_RENDER_MODE in self.configurate_state:
            item: RadioItem[RenderMode] = event.radio_set.children[event.index]
            event.radio_set._selected = event.index
            config.image.render_mode = item.data
            config.refresh()
            self.notify(ll.get('nofys.config.saved'), timeout=1.0)
            logger.trace(f'Updated [yellow]config.image.render_mode[/yellow]={config.image.render_mode!r}')
    
    @on(RadioSet.Changed, '#configurate-log-level-radioset')
    async def action_image_render_mode_changed(self, event: RadioSet.Changed) -> None:
        item: RadioItem[TextualLogLevel] = item_by_attr(event.radio_set._nodes, 'data', config.main.log_level)
        event.radio_set._selected = event.radio_set._nodes.index(item)
        event.pressed.value = False
        item.value = True
        self.notify(ll.get('nofys.function.disabled'), timeout=3.0, severity='warning')
    
    # ^ Compose
    
    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(classes='configurations-container') as configurations_container:
            yield from self.create_configurate_language(config, ll)
            yield from self.create_configurate_device_id(config, ll)
            yield from self.create_configurate_image_resample_method(config, ll)
            yield from self.create_configurate_image_render_mode(config, ll)
            yield from self.create_configurate_log_level(config, ll)
        configurations_container.border_title = ll.get('configurate')
        yield Footer()