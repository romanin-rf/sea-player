from pathlib import Path
from pydantic import BaseModel
from textual.binding import Binding
# > Typing
from types import ModuleType
from typing import (
    Any,
    Dict,
    List,
    Type,
    Tuple,
    Union,
    Optional,
    Callable,
    Generator,
    AsyncGenerator
)
# > Local Import's
from .pluginbase import PluginBase, PluginInfo
from ..seaplayer import SeaPlayer

# ! Types
class PluginModuleType(ModuleType):
    __plugin__: Type[PluginBase]

INFO_FILE_PATH = str
INIT_FILE_PATH = str
DEPS_FILE_PATH = str

# ! Functions
def get_module_info(path: str) -> Tuple[str, str]: ...
def load_module(path: str) -> PluginModuleType: ...
def plugin_from_module(app: SeaPlayer, pl: PluginLoader, info: PluginInfo, module: PluginModuleType) -> PluginBase: ...
def load_plugin_info(path: str) -> PluginInfo: ...

# ! Plugin Loader Config
class PluginLoaderConfigModel(BaseModel):
    plugins_enable: Dict[str, bool] = {}

class PluginLoaderConfigManager:
    filepath: Path
    """The path to the plugin configuration file."""
    config: PluginLoaderConfigModel
    """Contains attributes from the plugin configuration file."""
    
    @staticmethod
    def dump(path: str, data: PluginLoaderConfigModel) -> None:
        """Overwriting configurations.
        
        Args:
            path (str): The path to the plugin configuration file.
            data (PluginLoaderConfigModel): Contains attributes from the plugin configuration file.
        """
        ...
    @staticmethod
    def load(path: str, default_data: Dict[str, Any]) -> PluginLoaderConfigModel:
        """Loading configurations.
        
        Args:
            path (str): The path to the plugin configuration file.
            default_data (Dict[str, Any]): The standard values of the configuration file.
        
        Returns:
            PluginLoaderConfigModel: Contains attributes from the plugin configuration file.
        """
        ...
    def refresh(self) -> None: ...
    def __init__(self, path: str) -> None: ...
    def exists_plugin(self, info: PluginInfo) -> bool: ...
    def exists_plugin_by_name_id(self, name_id: str) -> bool: ...
    def add_plugin(self, info: PluginInfo) -> None: ...
    def remove_plugin(self, info: PluginInfo) -> None: ...
    def remove_plugin_by_name_id(self, name_id: str) -> None: ...
    def is_enable_plugin(self, info: PluginInfo) -> bool: ...
    def disable_plugin(self, info: PluginInfo) -> None: ...
    def disable_plugin_by_name_id(self, name_id: str) -> None: ...
    def enable_plugin(self, info: PluginInfo) -> None: ...
    def enable_plugin_by_name_id(self, name_id: str) -> None: ...

# ! Plugin Loader Class
class PluginLoader:
    app: SeaPlayer
    """A link to the image of the `SeaPlayer` class."""
    plugins_dirpath: Path
    """The path to the plugin folder."""
    plugins_config_path: Path
    """The path to the plugin loader configuration file."""
    on_plugins: List[PluginBase]
    """A list with initialized plugin classes."""
    off_plugins: List[PluginInfo]
    """A list with disabled plugins (more precisely, with information about them)."""
    error_plugins: List[Tuple[str, str]]
    """A list with plugins (more precisely, with the paths to them) that could not be loaded."""
    value_handlers: List[Callable[[str], List[str]]]
    
    def __init__(
        self,
        app: SeaPlayer,
        plugins_dirpath: Optional[Union[str, Path]]=None,
        plugins_config_path: Optional[Union[str, Path]]=None,
        *args,
        **kwargs
    ) -> None:
        ...
    # ! Magic Methods
    def __getitem__(self, key: str) -> Optional[PluginBase]: ...
    
    # ! Plugin Loader Methods
    @staticmethod
    async def aio_search_plugins_paths() -> AsyncGenerator[Tuple[INIT_FILE_PATH, INFO_FILE_PATH, Optional[DEPS_FILE_PATH]]]: ...
    @staticmethod
    def search_plugins_paths() -> Generator[Tuple[INIT_FILE_PATH, INFO_FILE_PATH, Optional[DEPS_FILE_PATH]], Any, None]: ...
    
    # ! App Specific Methods
    def on_bindings(self) -> Generator[Binding, Any, None]: ...
    
    # ! App On Methods
    def on_init(self) -> None: ...
    def on_run(self) -> None: ...
    async def on_compose(self) -> None: ...
    async def on_ready(self) -> None: ...
    async def on_quit(self) -> None: ...
