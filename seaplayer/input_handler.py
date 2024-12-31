import os
import glob
from uuid import UUID
from abc import ABC, abstractmethod
from seaplayer_audio import FileAudioSource
# > Typing
from typing_extensions import (
    Any,
    Generator,
)
# > Local Imports
from seaplayer.track import Playbacker, Track

# ! Abstract Class

class InputHandlerBase(ABC):
    def __init__(self, playbacker: Playbacker) -> None:
        self.playbacker = playbacker
    
    @abstractmethod
    def is_this(self, input: str, /) -> bool:
        return False
    
    @abstractmethod
    def handle(self, input: str, **kwargs) -> Generator[UUID, Any, None]:
        yield from []

# ! File/Glob Handler Class

class FileGlobInputHandler(InputHandlerBase):
    def is_this(self, input: str, /) -> bool:
        return glob.has_magic(input) or os.path.isfile(input)
    
    def __exist_track_by_filepath(self, filepath: str) -> bool:
        for track in self.playbacker.tracks.values():
            if track.source.name is not None:
                if os.path.samefile(filepath, track.source.name):
                    return True
        return False
    
    def handle(self, input: str, **kwargs) -> Generator[UUID, Any, None]:
        yield from []
        for filepath in glob.glob(input, recursive=True):
            if not self.__exist_track_by_filepath(filepath):
                try:
                    source = FileAudioSource(filepath, **kwargs)
                    yield Track(source, self.playbacker).uuid
                except:
                    pass