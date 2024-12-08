import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader as Loader, Dumper as Dumper
from pathlib import Path
# > Typing
from typing_extensions import (
    Dict, Any,
    Union, Literal,
    Self,
    _T as DT
)
# > Local Imports
from ._types import FilePathType

# ! Variables

# ! Main Config Class

class Config:
    __default_config_data__ = {
        "main.language": "en-eng"
    }
    
    # ^ Methods
    
    @staticmethod
    def __dump(
        filepath: str,
        data: Dict[str, Any]
    ) -> None:
        with open(filepath, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, Dumper=Dumper, sort_keys=False)
    
    @staticmethod
    def __load(
        filepath: str,
        default: Dict[str, Any]
    ) -> Dict[str, Any]:
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return yaml.load(file, Loader=Loader)
        except:
            Config.__dump(filepath, default)
            return default
    
    # ^ Init
    def __init__(
        self,
        config_filepath: FilePathType,
    ) -> None:
        self._filepath = Path(config_filepath).absolute()
        self._data = self.__load(self._filepath, self.__default_config_data__)
    
    # ^ Dander Methods
    
    def __getitem__(self, key: str):
        return self._data[key]
    
    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value
    
    def __iadd__(self, other: 'Config') -> Self:
        self._data.update(other._data)
        return self
    
    # ^ Config Methods
    
    def get(self, key: str, default: Union[DT, Any]=None) -> Union[DT, Any]:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default
    
    def set(self, key: str, value: Any) -> None:
        self.__setitem__(key, value)
    
    def merge(self, config: 'Config') -> None:
        self._data.update(config._data)
    
    # ^ Propertyes
    
    @property
    def main_language(self) -> Union[str, Literal['en-eng']]:
        return self.get("main.language", "en-eng")

# ! Start
if __name__ == "__main__":
    config = Config("./test-config.yaml")