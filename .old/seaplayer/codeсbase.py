import os
from typing import Optional

# ! Functions
def formater(**kwargs) -> str:
    return ", ".join([f"{key}={repr(value)}" for key, value in kwargs.items()])

# ! Codecs Base
class CodecBase:
    """The base class of the codec."""
    # * Codec Info
    codec_name: str="None"
    """The name of the codec (abbreviation)."""
    codec_priority: float=0.0
    """Sorting priority (the lower the value, the earlier it will be processed, checked for compatibility and initialized)"""
    
    # * Info
    name: str
    """File path (optional file path)."""
    hidden_name: bool=False
    """Hide the `name` when displayed in the SeaPlayer."""
    duration: float
    """The duration of the sound in seconds."""
    channels: int
    """The number of channels in the file."""
    samplerate: int
    """The sampling rate in hertz (Hz)."""
    bitrate: int
    """The number of bits per second of playback (determines the sound quality)."""
    
    # * Sound Info
    title: Optional[str]
    """The `title` of the sound is taken from the metadata."""
    artist: Optional[str]
    """The `artist` is taken from the metadata."""
    album: Optional[str]
    """The `album title` is taken from the metadata."""
    icon_data: Optional[bytes]
    """A `poster` in bytes format is obtained from metadata."""
    
    # * Playback Info
    playing: bool
    """The playback status (`True if playing`)."""
    paused: bool
    """The playback status (`True if paused`)."""
    
    # ! Initializing Functions
    def __init__(self, path: str, **kwargs) -> None:
        """The base class of the codec.
        
        Args:
            path (str): File path (optional file path).
        """
        ...
    #async def __aio_init__(self, path: str, **kwargs) -> None: ...
    def __repr__(self):
        return \
            "{0}({1})".format(
                self.__class__.__name__,
                formater(
                    name=self.name,
                    duration=self.duration,
                    channels=self.channels,
                    samplerate=self.samplerate,
                    bitrate=self.bitrate,
                    title=self.title,
                    artist=self.artist,
                    album=self.album
                )
            )
    
    def __namerepr__(self) -> str:
        """The name that is displayed for the place `self.name`.
        
        Returns:
            str: Value `self.name` the displayed in SeaPlayer.
        """
        if self.hidden_name:
            return ""
        if self.name is not None:
            return self.name
        return f'<memory>'
    
    def __headrepr__(self) -> str:
        """The display name in the SeaPlayer.
        
        Returns:
            str: Value `self.title` + `self.artist` the displayed in SeaPlayer.
        """
        if self.hidden_name:
            if (self.title is not None):
                if self.artist is not None:
                    return f"{self.artist} - {self.title}"
                return self.title
            return "<hidden>"
        if self.name is not None:
            return os.path.basename(self.name)
        return self.__namerepr__()
    
    def __sha1__(self, buffer_size: int) -> str:
        """Calculating the hash of the file.
        
        Args:
            buffer_size (int): The size of the temporary buffer.
        
        Returns:
            str: SHA256 in string format.
        """
        ...
    
    async def __aio_sha1__(self, buffer_size: int) -> str:
        """Calculating the hash of the file.
        
        Args:
            buffer_size (int): The size of the temporary buffer.
        
        Returns:
            str: SHA256 in string format.
        """
        ...
    
    # ! Testing Functions
    @staticmethod
    def is_this_codec(path: str) -> bool:
        """Compatibility check.
        
        Args:
            path (str): File path (optional file path).
        
        Returns:
            bool: True if compatible.
        """
        return False
    
    @staticmethod
    async def aio_is_this_codec(path: str) -> bool:
        """Compatibility check.
        
        Args:
            path (str): File path (optional file path).
        
        Returns:
            bool: True if compatible.
        """
        return False
    
    # ! Playback Functions
    def play(self) -> None:
        """Start playing the sound."""
        ...
    
    def stop(self) -> None:
        """Stop playing the sound."""
        ...
    
    def pause(self) -> None:
        """Put it on pause."""
        ...
    
    def unpause(self) -> None:
        """Take it off the pause."""
        ...
    
    def get_volume(self) -> float:
        """Getting the current volume as a percentage.
        
        Returns:
            float: Volume percentage (0.01 == 1%).
        """
        return 1.0
    
    def set_volume(self, value: float) -> None:
        """Setting the volume value as a percentage.
        
        Args:
            value (float): Volume percentage (0.01 == 1%).
        """
        ...
    
    def get_pos(self) -> float:
        """Getting the audio playback position in seconds.
        
        Returns:
            float: The position of the audio playback in seconds.
        """
        return 0.0
    
    def set_pos(self, value: float) -> None:
        """Setting the audio playback position in seconds.
        
        Args:
            value (float): The position of the audio playback in seconds.
        """
        ...
