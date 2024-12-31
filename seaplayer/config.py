import yaml
try:
    from yaml import CSafeLoader as Loader, CSafeDumper as Dumper
except ImportError:
    from yaml import SafeLoader as Loader, SafeDumper as Dumper
from pathlib import Path
from pydantic import BaseModel, Field, ValidationError
# > Typing
from typing_extensions import (
    Optional,
)
# > For Typing
from PIL.Image import Resampling
# > Local Imports
from ._types import FilePathType
from .objects.image import RenderMode

# ! Config Models

class ConfigMainModel(BaseModel):
    language: str = Field('en-eng', min_length=6, max_length=6)

class ConfigImageModel(BaseModel):
    resample: Resampling = Resampling.BILINEAR
    render_mode: Resampling = RenderMode.HALF

class ConfigSoundModel(BaseModel):
    output_device_id: Optional[int]=None
    max_volume: float = 3.0
    volume_per: float = 0.05
    rewind_per: int = 5

class ConfigKeyModel(BaseModel):
    quit: str               = 'q,й'
    rewind_forward: str     = '],*'
    rewind_backward: str    = '[,/'
    volume_add: str         = '+,='
    volume_drop: str        = '-'

class ConfigModel(BaseModel):
    main: ConfigMainModel = ConfigMainModel()
    image: ConfigImageModel = ConfigImageModel()
    sound: ConfigSoundModel = ConfigSoundModel()
    key: ConfigKeyModel = ConfigKeyModel()

# ! Main Config Class

class Config:
    __default_config_data__ = ConfigModel()
    
    # ^ Methods
    
    @staticmethod
    def __dump(
        filepath: str,
        data: ConfigModel
    ) -> None:
        with open(filepath, 'w', encoding='utf-8') as file:
            yaml.dump(data.model_dump(mode='json', warnings=False), file, Dumper, sort_keys=False)
    
    @staticmethod
    def __load(
        filepath: str,
        default: ConfigModel
    ) -> ConfigModel:
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return ConfigModel.model_validate(yaml.load(file, Loader), strict=False)
        except ValidationError:
            Config.__dump(filepath, default)
            return default
    
    # ^ Init
    def __init__(
        self,
        config_filepath: FilePathType,
    ) -> None:
        self._filepath = Path(config_filepath).absolute()
        self._data = self.__load(self._filepath, self.__default_config_data__)
    
    def refresh(self) -> None:
        self.__dump(self._filepath, self._data)
    
    # ^ Propertyes
    
    @property
    def main(self) -> ConfigMainModel:
        return self._data.main
    
    @property
    def image(self) -> ConfigImageModel:
        return self._data.image
    
    @property
    def sound(self) -> ConfigSoundModel:
        return self._data.sound
    
    @property
    def key(self) -> ConfigKeyModel:
        return self._data.key

# ! Start
if __name__ == "__main__":
    config = Config("./test-config.yaml")
    config.refresh()