from pathlib import Path
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

FilePathType: TypeAlias = Union[str, Path]

SupportAudioSource: TypeAlias = Union[AsyncFileAudioSource]
SupportAudioStreamer: TypeAlias = Union[AsyncCallbackSoundDeviceStreamer, AsyncThreadSoundDeviceStreamer]

# ! Playback Types

class PlaybackMode(Enum):
    PLAY = 0
    REPLAY_SOUND = 1
    REPLAY_LIST = 2