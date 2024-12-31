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
from seaplayer.units import config, ll
from seaplayer.config import Config
from seaplayer.languages import LanguageLoader
from seaplayer.objects.image import RenderMode
from seaplayer.objects.optionitem import OptionItem
from seaplayer.objects.radioitem import RadioItem

# ! Types

class ConfigurateState(Flag):
    LANGUAGE = auto()
    DEVICE_ID = auto()
    IMAGE_RESAMPLING = auto()
    IMAGE_RENDER_MODE = auto()

# ! Methods

def _rr(_: bool):
    if _:
        return ' [red]\\[%s][/red]' % ll.get('words.restart_required')
    return ''

# ! Main Configration Screen

class ConfigurationScreen(Screen):
    BINDINGS = [
        Binding('escape', 'app.pop_screen', 'Close', priority=True),
    ]
    SUB_TITLE = 'Configuration'
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
    
    # ^ Configurate Parameters
    
    def create_configurate_language(self, config: Config, ll: LanguageLoader) -> ComposeResult:
        yield from []
        if ConfigurateState.LANGUAGE not in self.configurate_state:
            with Container(classes='configuration-item-container') as container:
                container.border_title = ll.get('configurate.main.lang')
                container.border_subtitle = ll.get('configurate.main.lang.desc') + _rr(True)
                options, selected_index = [], 0
                for index, lang in enumerate(ll.langs):
                    if lang.author_url is not None:
                        options.append(
                            OptionItem(f"{lang.title} ({lang.words['from']} [link={lang.author_url}]{lang.author}[/link])", lang.mark)
                        )
                    else:
                        options.append(
                            OptionItem(f"{lang.title} ({lang.words['from']} {lang.author})", lang.mark)
                        )
                    if config.main.language == lang.mark:
                        selected_index = index
                yield (option_list := OptionList(*options, id='configurate-language-optionlist'))
                container.styles.height = len(options)+4
                option_list.highlighted = selected_index
            self.configurate_state |= ConfigurateState.LANGUAGE
    
    def create_configurate_device_id(self, config: Config, ll: LanguageLoader) -> ComposeResult:
        yield from []
    
    def create_configurate_image_resample_method(self, config: Config, ll: LanguageLoader) -> ComposeResult:
        yield from []
        if ConfigurateState.IMAGE_RESAMPLING not in self.configurate_state:
            variants = (
                (ll.get('configurate.image.resample_method.nearest'), Resampling.NEAREST),
                (ll.get('configurate.image.resample_method.lanczos'), Resampling.LANCZOS),
                (ll.get('configurate.image.resample_method.bilinear'), Resampling.BILINEAR),
                (ll.get('configurate.image.resample_method.bicubic'), Resampling.BICUBIC),
                (ll.get('configurate.image.resample_method.box'), Resampling.BOX),
                (ll.get('configurate.image.resample_method.hamming'), Resampling.HAMMING),
            )
            with Container(classes='configuration-item-container') as container:
                container.border_title = ll.get('configurate.image.resample_method')
                container.border_subtitle = ll.get('configurate.image.resample_method.desc') + _rr(True)
                length = 0
                with RadioSet(id='configurate-image-resample-radioset'):
                    for text, data in variants:
                        value = (config.image.resample == data)
                        length += 1
                        yield RadioItem(text, value, data=data)
                container.styles.height = length + 4
            self.configurate_state |= ConfigurateState.IMAGE_RESAMPLING
    
    def create_configurate_image_render_mode(self, config: Config, ll: LanguageLoader) -> ComposeResult:
        yield from []
        if ConfigurateState.IMAGE_RENDER_MODE not in self.configurate_state:
            variants = (
                (ll.get('configurate.image.render_mode.none'), RenderMode.NONE),
                (ll.get('configurate.image.render_mode.half'), RenderMode.FULL),
                (ll.get('configurate.image.render_mode.full'), RenderMode.HALF),
            )
            with Container(classes='configuration-item-container') as container:
                container.border_title = ll.get('configurate.image.render_mode')
                container.border_subtitle = ll.get('configurate.image.render_mode.desc') + _rr(True)
                length = 0
                with RadioSet(id='configurate-image-render-mode-radioset'):
                    for text, data in variants:
                        value = (config.image.render_mode == data)
                        length += 1
                        yield RadioItem(text, value, data=data)
                container.styles.height = length + 4
            self.configurate_state |= ConfigurateState.IMAGE_RENDER_MODE
    
    # ^ Callbacks
    
    @on(OptionList.OptionSelected, '#configurate-language-optionlist')
    async def action_language_selected(self, event: OptionList.OptionSelected) -> None:
        if ConfigurateState.LANGUAGE in self.configurate_state:
            item: OptionItem[str] = event.option
            config.main.language = item.data
            config.refresh()
            self.notify(ll.get('nofys.config.saved'), timeout=1.0)
    
    @on(RadioSet.Changed, '#configurate-image-resample-radioset')
    async def action_image_resample_changed(self, event: RadioSet.Changed) -> None:
        if ConfigurateState.IMAGE_RESAMPLING in self.configurate_state:
            item: RadioItem[Resampling] = event.radio_set.children[event.index]
            config.image.resample = item.data
            config.refresh()
            self.notify(ll.get('nofys.config.saved'), timeout=1.0)
    
    @on(RadioSet.Changed, '#configurate-image-render-mode-radioset')
    async def action_image_render_mode_changed(self, event: RadioSet.Changed) -> None:
        if ConfigurateState.IMAGE_RENDER_MODE in self.configurate_state:
            item: RadioItem[RenderMode] = event.radio_set.children[event.index]
            config.image.render_mode = item.data
            config.refresh()
            self.notify(ll.get('nofys.config.saved'), timeout=1.0)
    
    # ^ Compose
    
    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(classes='configurations-container') as configurations_container:
            yield from self.create_configurate_language(config, ll)
            yield from self.create_configurate_image_resample_method(config, ll)
            yield from self.create_configurate_image_render_mode(config, ll)
        configurations_container.border_title = ll.get('configurate')
        yield Footer()