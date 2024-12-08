
# ! Metadata
__prog_name__ = 'seaplug'
__prog_title__ = 'SeaPlayer Plugins System CLI'
__prog_version__ = '0.3.0'
__prog_author__ = 'Romanin'
__prog_email__ = 'semina054@gmail.com'

# ! Vars
CREATE_DEFAULT_CODE = """\
from seaplayer.plug import PluginBase

class Plugin(PluginBase):
    pass

__plugin__ = Plugin
"""