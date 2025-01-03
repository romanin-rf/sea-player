from textual.binding import Binding, BindingType
# > Local Imports
from seaplayer.config import Config
from seaplayer.languages import LanguageLoader
# > Screen Imports
from seaplayer.screens.log import LogScreen
from seaplayer.screens.configurator import ConfigurationScreen
# > Typing
from typing_extensions import Iterator

# ! Variables

SCREENS = {
    'configurator': ConfigurationScreen,
    'log': LogScreen
}

# ! Methods

def screens_bindings(config: Config, ll: LanguageLoader) -> Iterator[BindingType]:
    yield Binding('c,с', "smart_push_screen('configurator')", ll.get('configurate'))
    yield Binding('l,д', "smart_push_screen('log')", ll.get('footer.logs'))

# ! Annotations

__all__ = []