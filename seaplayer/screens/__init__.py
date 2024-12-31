from textual.binding import Binding, BindingType
# > Local Imports
from seaplayer.config import Config
from seaplayer.languages import LanguageLoader
from seaplayer.screens.configurator import ConfigurationScreen
# > Typing
from typing_extensions import Iterator

# ! Variables

SCREENS = {
    'configurator': ConfigurationScreen
}

# ! Methods

def screens_bindings(config: Config, ll: LanguageLoader) -> Iterator[BindingType]:
    yield Binding('c,с', "smart_push_screen('configurator')", ll.get('configurate'))

# ! Annotations

__all__ = []