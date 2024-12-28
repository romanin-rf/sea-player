import yaml
import json
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader as Loader, Dumper as Dumper
from pathlib import Path
from pydantic import BaseModel, Field
# > Typing
from typing_extensions import (
    Annotated
)
# > For Typing
from PIL.Image import Resampling
# > Local Imports
from ._types import FilePathType
from .objects.image import RenderMode

# ! Validators & Serializers Methods

# ! Types

# ! Config Models

class ConfigMainModel(BaseModel):
    language: str = Field('en-eng', min_length=6, max_length=6)

class ConfigImageModel(BaseModel):
    resample: Resampling = Resampling.BILINEAR
    render_mode: Resampling = RenderMode.HALF

class ConfigSoundModel(BaseModel):
    max_volume: float = Field(3.0)

class ConfigModel(BaseModel):
    main: ConfigMainModel = ConfigMainModel()
    image: ConfigImageModel = ConfigImageModel()
    sound: ConfigSoundModel = ConfigSoundModel()
    
    def __setstate__(self, state):
        return super().__setstate__(state)

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
                return ConfigModel.model_validate(yaml.load(file, Loader=Loader))
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
    
    def refresh(self) -> None:
        self.__dump(self._filepath, self._data)
    
    # ^ Propertyes
    
    @property
    def main(self) -> ConfigMainModel:
        return self._data.main
    
    @property
    def image(self) -> ConfigImageModel:
        return self._data.image

# ! Start
if __name__ == "__main__":
    config = Config("./test-config.yaml")
    config.refresh()