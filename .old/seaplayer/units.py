import os
import sys
from platformdirs import user_config_dir
# > Image Works
from PIL.Image import Resampling

# ! Metadata
__title__ = "SeaPlayer"
__version__ = "0.8.11"
__author__ = "Romanin"
__email__ = "semina054@gmail.com"
__url__ = "https://github.com/romanin-rf/SeaPlayer"

# ! Paths
IM_BINARY = (bool(getattr(sys, 'frozen', False)) and hasattr(sys, '_MEIPASS'))
if IM_BINARY:
    LOCALDIR = os.path.dirname(sys.executable)
    ENABLE_PLUGIN_SYSTEM = False
else:
    LOCALDIR = os.path.dirname(os.path.dirname(__file__))
    ENABLE_PLUGIN_SYSTEM = True

# ! SeaPlayer Paths
CSS_LOCALDIR = os.path.join(os.path.dirname(__file__), "css")
ASSETS_DIRPATH = os.path.join(os.path.dirname(__file__), "assets")
CONFIG_DIRPATH = user_config_dir(__title__, __author__, ensure_exists=True)
CONFIG_FILEPATH = os.path.join(CONFIG_DIRPATH, "config.properties")
CACHE_DIRPATH = os.path.join(CONFIG_DIRPATH, "cache")
LANGUAGES_DIRPATH = os.path.join(LOCALDIR, "seaplayer", "langs")

# ! PluginLoader Paths
PLUGINS_DIRPATH = os.path.join(CONFIG_DIRPATH, "plugins")
PLUGINS_CONFIG_PATH = os.path.join(CONFIG_DIRPATH, "plugins.json")

# ! Glob pattern-paths
GLOB_PLUGINS_INFO_SEARCH = os.path.join(PLUGINS_DIRPATH, "*", "info.json")
GLOB_PLUGINS_INIT_SEARCH = os.path.join(PLUGINS_DIRPATH, "*", "__init__.py")
GLOB_PLUGINS_DEPS_SEARCH = os.path.join(PLUGINS_DIRPATH, "*", "requirements.txt")

# ! Assets Paths
IMGPATH_IMAGE_NOT_FOUND = os.path.join(ASSETS_DIRPATH, "image-not-found.png")

# ! Constants
RESAMPLING_SAFE = {
    "nearest": Resampling.NEAREST,
    "bilinear": Resampling.BILINEAR,
    "bicubic": Resampling.BICUBIC,
    "lanczos": Resampling.LANCZOS,
    "hamming": Resampling.HAMMING,
    "box": Resampling.BOX
}