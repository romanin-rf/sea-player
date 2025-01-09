from os import PathLike
from pathlib import Path, PurePath, PosixPath, PurePosixPath, PureWindowsPath, WindowsPath
from enum import Enum
# > Typing
from typing_extensions import (
    TypeAlias
)
# > Local Imports
from seaplayer_audio import MPSoundDeviceStreamer
from seaplayer_audio.audiosources import FileAudioSource

# ! Type Aliases

PathlibType: TypeAlias = Path | PurePath | PosixPath | PurePosixPath | PureWindowsPath | WindowsPath
FilePathType: TypeAlias = str | bytes | PathlibType | PathLike[str] | PathLike[bytes]

SupportAudioSource: TypeAlias = FileAudioSource
SupportAudioStreamer: TypeAlias = MPSoundDeviceStreamer

# ! Playback Types

class PlaybackMode(Enum):
    PLAY = 0
    REPLAY_SOUND = 1
    REPLAY_LIST = 2
