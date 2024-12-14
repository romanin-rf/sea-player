from os import PathLike
from pathlib import Path, PurePath, PosixPath, PurePosixPath, PureWindowsPath, WindowsPath
from enum import Enum
# > Typing
from typing_extensions import (
    Union,
    TypeAlias
)
# > Local Imports
from seaplayer_audio.audiosources import AsyncFileAudioSource
from seaplayer_audio.streamers import AsyncCallbackSoundDeviceStreamer, AsyncThreadSoundDeviceStreamer

# ! Type Aliases

PathlibType: TypeAlias = Union[Path, PurePath, PosixPath, PurePosixPath, PureWindowsPath, WindowsPath]
FilePathType: TypeAlias = Union[str, bytes, PathlibType, PathLike[str], PathLike[bytes]]

SupportAudioSource: TypeAlias = Union[AsyncFileAudioSource]
SupportAudioStreamer: TypeAlias = Union[AsyncCallbackSoundDeviceStreamer, AsyncThreadSoundDeviceStreamer]

# ! Playback Types

class PlaybackMode(Enum):
    PLAY = 0
    REPLAY_SOUND = 1
    REPLAY_LIST = 2