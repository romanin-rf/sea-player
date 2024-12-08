import properties
from pathlib import Path
from typing import Dict, Any, Optional, TypeVar, Union, Literal

# ! Types
T = TypeVar("T")

# ! Vars
DEFAULT_CONFIG_DATA: Dict[str, Any] = {
    "main.lang": "en-eng",
    "sound.sound_font_path": None,
    "sound.output_sound_device_id": None,
    "image.image_update_method": "sync",
    "image.image_resample_method": "bilinear",
    "playback.rewind_count_seconds": 5,
    "playback.volume_change_percent": 0.05,
    "playback.max_volume_percent": 2.0,
    "playlist.recursive_search": False,
    "keys.quit": "q,й",
    "keys.rewind_forward": "*",
    "keys.rewind_back": "/",
    "keys.volume_up": "+",
    "keys.volume_down": "-",
    "debag.logging": False
}
"""Default configuration values."""

# ! Main Class
class SeaPlayerConfig:
    """The main configuration class of the SeaPlayer."""
    @staticmethod
    def dump(filepath: Path, data: Dict[str, Any]) -> None:
        with open(filepath, "w", encoding="utf-8", errors="ignore") as file:
            properties.dump(data, file)
    
    @staticmethod
    def load(filepath: Path, default: Dict[str, Any]) -> Dict[str, Any]:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
            try:
                return properties.load(file)
            except:
                pass
        with open(filepath, "w", encoding="utf-8", errors="ignore") as file:
            properties.dump(default, file)
        return default
    
    def refresh(self) -> None:
        """Overwriting configurations to a file."""
        self.dump(self.filepath, self.config)
    
    def __init__(
        self,
        filepath: str,
        *,
        default_data: Dict[str, Any]=DEFAULT_CONFIG_DATA
    ) -> None:
        """The main configuration class of the SeaPlayer.
        
        Args:
            filepath (str): The path to the configuration file.
            default_data (Dict[str, Any], optional): Default configuration values. Defaults to DEFAULT_CONFIG_DATA.
        """
        self.filepath = Path(filepath)
        self.default_data = default_data
        if self.filepath.exists():
            self.config = self.load(self.filepath, self.default_data)
            config_temp = self.default_data.copy()
            config_temp.update(self.config)
            self.config = config_temp.copy()
            del config_temp
        else:
            self.config = default_data.copy()
        self.refresh()
    
    def get(self, key: str, default: T=None) -> Union[Any, T]:
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        self.config[key] = value
        self.refresh()
    
    # ! Main
    @property
    def lang(self) -> Union[Literal['en-eng'], str]:
        """The current language.
        
        Returns:
            The file name without an extension.
        """
        return self.get("main.lang")
    @lang.setter
    def lang(self, value: Union[Literal['en-eng'], str]) -> None: self.set("main.lang", value)
    
    # ! Sound
    @property
    def sound_font_path(self) -> Optional[str]:
        """The path to the file with the audio font.
        
        Returns:
            The full path to the file.
        """
        return self.get("sound.sound_font_path")
    @sound_font_path.setter
    def sound_font_path(self, value: Optional[str]): self.set("sound.sound_font_path", value)
    
    @property
    def output_sound_device_id(self) -> Optional[int]:
        """ID of the audio output device.
        
        Returns:
            The device ID.
        """
        return self.get("sound.output_sound_device_id")
    @output_sound_device_id.setter
    def output_sound_device_id(self, value: Optional[int]): self.set("sound.output_sound_device_id", value)
    
    # ! Image
    @property
    def image_update_method(self) -> Literal["sync", "async"]: return self.get("image.image_update_method")
    @image_update_method.setter
    def image_update_method(self, value: Literal["sync", "async"]): self.set("image.image_update_method", value)
    
    @property
    def image_resample_method(self) -> Literal["nearest", "bilinear", "bicubic", "lanczos", "hamming", "box"]:
        """The image resampling method.
        
        Returns:
            The image resampling method.
        """
        return self.get("image.image_resample_method")
    @image_resample_method.setter
    def image_resample_method(self, value: Literal["nearest", "bilinear", "bicubic", "lanczos", "hamming", "box"]):
        self.set("image.image_resample_method", value)
    
    # ! Playback
    @property
    def volume_change_percent(self) -> float:
        """Percentage by which the volume changes when the special keys are pressed.
        
        Returns:
            Value 0.01 == 1%.
        """
        return self.get("playback.volume_change_percent")
    @volume_change_percent.setter
    def volume_change_percent(self, value: float): self.set("playback.volume_change_percent", value)
    
    @property
    def rewind_count_seconds(self) -> int:
        """The value of the seconds by which the current sound will be rewound.
        
        Returns:
            Rewind in seconds.
        """
        return self.get("playback.rewind_count_seconds")
    @rewind_count_seconds.setter
    def rewind_count_seconds(self, value: int): self.set("playback.rewind_count_seconds", value)
    
    @property
    def max_volume_percent(self) -> float:
        """Maximum volume value.
        
        Returns:
            Value 0.01 == 1%.
        """
        return self.get("playback.max_volume_percent")
    @max_volume_percent.setter
    def max_volume_percent(self, value: float): self.set("playback.max_volume_percent", value)
    
    # ! Playlist
    @property
    def recursive_search(self) -> bool:
        """Recursive file search.
        
        Returns:
            On or off.
        """
        return self.get("playlist.recursive_search")
    @recursive_search.setter
    def recursive_search(self, value: bool): self.set("playlist.recursive_search", value)
    
    # ! Keys
    @property
    def key_quit(self) -> str:
        """The key to exit the SeaPlayer.
        
        Returns:
            The key char(s).
        """
        return self.get("keys.quit")
    @key_quit.setter
    def key_quit(self, value: str): self.set("keys.quit", value)
    
    @property
    def key_rewind_forward(self) -> str:
        """The rewind forward key.
        
        Returns:
            The key char(s).
        """
        return self.get("keys.rewind_forward")
    @key_rewind_forward.setter
    def key_rewind_forward(self, value: str): self.set("keys.rewind_forward", value)
    
    @property
    def key_rewind_back(self) -> str:
        """The rewind back key.
        
        Returns:
            The key char(s).
        """
        return self.get("keys.rewind_back")
    @key_rewind_back.setter
    def key_rewind_back(self, value: str): self.set("keys.rewind_back", value)
    
    @property
    def key_volume_up(self) -> str:
        """The volume up key.
        
        Returns:
            The key char(s).
        """
        return self.get("keys.volume_up")
    @key_volume_up.setter
    def key_volume_up(self, value: str): self.set("keys.volume_up", value)
    
    @property
    def key_volume_down(self) -> str:
        """The volume down key.
        
        Returns:
            The key char(s).
        """
        return self.get("keys.volume_down")
    @key_volume_down.setter
    def key_volume_down(self, value: str): self.set("keys.volume_down", value)
    
    # ! Debag
    @property
    def logging(self) -> bool:
        """Enabling and disabling logging.
        
        Returns:
            On or off.
        """
        return self.get("debag.logging")
    @logging.setter
    def logging(self, value: bool): self.set("debag.logging", value)
