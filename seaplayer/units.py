import os
import sys
import importlib.metadata
from platformdirs import user_config_dir
# > Pillow
from PIL import Image
# > Local Imports
from seaplayer.config import Config
from seaplayer.languages import LanguageLoader
from seaplayer.others.cache import Cacher
from seaplayer.objects.log import TextualLogger, TextualLogLevel

# ! Metadata

__title__                   = "SeaPlayer"
__version__                 = "0.10.0.dev35"
__author__                  = "Romanin"
__email__                   = "semina054@gmail.com"
__url__                     = "https://github.com/romanin-rf/SeaPlayer"

# ! Initialization

IM_NUITKA_BINARY            = "__compiled__" in globals()
IM_PYINSTALLER_BINARY       = bool(getattr(sys, 'frozen', False)) and hasattr(sys, '_MEIPASS')
IM_BINARY                   = IM_NUITKA_BINARY or IM_PYINSTALLER_BINARY
if IM_BINARY:
    LOCAL_DIRPATH           = os.path.dirname(os.path.abspath(sys.argv[0]))
    #ENABLE_PLUGIN_SYSTEM    = False
else:
    LOCAL_DIRPATH           = os.path.dirname(os.path.abspath(__file__))
    #ENABLE_PLUGIN_SYSTEM    = True

# ! SeaPlayer Paths

CSS_LOCALDIR                = os.path.join(LOCAL_DIRPATH, 'style')
ASSETS_DIRPATH              = os.path.join(LOCAL_DIRPATH, 'assets')
CONFIG_DIRPATH              = user_config_dir(__title__, False, ensure_exists=True)
CONFIG_FILEPATH             = os.path.join(CONFIG_DIRPATH, 'config.yaml')
CACHE_DIRPATH               = os.path.join(CONFIG_DIRPATH, 'cache')
LANGUAGES_DIRPATH           = os.path.join(LOCAL_DIRPATH, 'langs')

# ! PluginLoader Paths

#PLUGINS_DIRPATH = os.path.join(CONFIG_DIRPATH, "plugins")
#PLUGINS_CONFIG_PATH = os.path.join(CONFIG_DIRPATH, "plugins.json")

# ! Glob pattern-paths

#GLOB_PLUGINS_INFO_SEARCH = os.path.join(PLUGINS_DIRPATH, "*", "info.json")
#GLOB_PLUGINS_INIT_SEARCH = os.path.join(PLUGINS_DIRPATH, "*", "__init__.py")
#GLOB_PLUGINS_DEPS_SEARCH = os.path.join(PLUGINS_DIRPATH, "*", "requirements.txt")

# ! Assets Paths

IMGPATH_IMAGE_NOT_FOUND     = os.path.join(ASSETS_DIRPATH, "image-not-found.png")

# ! Assets Loading

IMG_NOT_FOUND               = Image.open(IMGPATH_IMAGE_NOT_FOUND)

# ! Variables

config: Config              = Config(CONFIG_FILEPATH)
cacher: Cacher              = Cacher(CACHE_DIRPATH)
ll: LanguageLoader          = LanguageLoader(LANGUAGES_DIRPATH, config.main.language)
logger: TextualLogger       = TextualLogger(config.main.log_level)

# ! Log

logger.debug('Package \"rich\" has [cyan]v{0}[/cyan]'.format(importlib.metadata.version('rich')))
logger.debug('Package \"textual\" has [cyan]v{0}[/cyan]'.format(importlib.metadata.version('textual')))
logger.debug('Package \"seaplayer\" has [cyan]v{0}[/cyan]'.format(__version__))
logger.debug('Package \"seaplayer-audio\" has [cyan]v{0}[/cyan]'.format(importlib.metadata.version('seaplayer-audio')))

logger.group('UNITS CONSTANTS', TextualLogLevel.DEBUG)

logger.debug(f'{IM_NUITKA_BINARY=!r}')
logger.debug(f'{IM_PYINSTALLER_BINARY=!r}')
logger.debug(f'{IM_BINARY=!r}')
logger.debug(f'{LOCAL_DIRPATH=!r}')
logger.debug(f'{CSS_LOCALDIR=!r}')
logger.debug(f'{ASSETS_DIRPATH=!r}')
logger.debug(f'{CONFIG_DIRPATH=!r}')
logger.debug(f'{CONFIG_FILEPATH=!r}')
logger.debug(f'{CACHE_DIRPATH=!r}')
logger.debug(f'{LANGUAGES_DIRPATH=!r}')

logger.group('ENV VARIABLES', TextualLogLevel.DEBUG)

for _key in os.environ:
    logger.debug(f'{_key}={os.environ[_key]!r}')

logger.group('UNITS LOG [yellow]ENDED[/yellow]', TextualLogLevel.DEBUG)