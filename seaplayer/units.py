import os
import sys
from platformdirs import user_config_dir
# > Pillow
from PIL import Image

# ! Metadata
__title__ = "SeaPlayer"
__version__ = "0.10.0"
__author__ = "Romanin"
__email__ = "semina054@gmail.com"
__url__ = "https://github.com/romanin-rf/SeaPlayer"

# ! Settings
#ENABLE_PLUGIN_SYSTEM_BUILD = False

# ! Initialization
IM_BINARY = (bool(getattr(sys, 'frozen', False)) and hasattr(sys, '_MEIPASS'))
if IM_BINARY:
    LOCALDIR = os.path.dirname(sys.executable)
    #ENABLE_PLUGIN_SYSTEM = False
else:
    LOCALDIR = os.path.dirname(os.path.dirname(__file__))
    #ENABLE_PLUGIN_SYSTEM = True

# ! SeaPlayer Paths
CSS_LOCALDIR = os.path.join(os.path.dirname(__file__), "style")
ASSETS_DIRPATH = os.path.join(os.path.dirname(__file__), "assets")
CONFIG_DIRPATH = user_config_dir(__title__, __author__, ensure_exists=True)
CONFIG_FILEPATH = os.path.join(CONFIG_DIRPATH, "config.yaml")
CACHE_DIRPATH = os.path.join(CONFIG_DIRPATH, "cache")
LANGUAGES_DIRPATH = os.path.join(LOCALDIR, "seaplayer", "langs")

# ! PluginLoader Paths
#PLUGINS_DIRPATH = os.path.join(CONFIG_DIRPATH, "plugins")
#PLUGINS_CONFIG_PATH = os.path.join(CONFIG_DIRPATH, "plugins.json")

# ! Glob pattern-paths
#GLOB_PLUGINS_INFO_SEARCH = os.path.join(PLUGINS_DIRPATH, "*", "info.json")
#GLOB_PLUGINS_INIT_SEARCH = os.path.join(PLUGINS_DIRPATH, "*", "__init__.py")
#GLOB_PLUGINS_DEPS_SEARCH = os.path.join(PLUGINS_DIRPATH, "*", "requirements.txt")

# ! Assets Paths
IMGPATH_IMAGE_NOT_FOUND = os.path.join(ASSETS_DIRPATH, "image-not-found.png")

# ! Assets Loading
IMG_NOT_FOUND = Image.open(IMGPATH_IMAGE_NOT_FOUND)