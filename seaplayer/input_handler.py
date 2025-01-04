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
from seaplayer.units import logger

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
    
    def _exist_track_by_filepath(self, filepath: str) -> bool:
        for track in self.playbacker.tracks.values():
            if track.source.name is not None:
                if os.path.samefile(filepath, track.source.name):
                    return True
        return False
    
    def handle(self, input: str, **kwargs) -> Generator[UUID, Any, None]:
        yield from []
        filespaths = glob.glob(input, recursive=True)
        logger.trace(f"Paths found: {filespaths!r}")
        for filepath in filespaths:
            if not self._exist_track_by_filepath(filepath):
                try:
                    source = FileAudioSource(filepath, **kwargs)
                    track = Track(source, self.playbacker)
                    yield track.uuid
                except:
                    logger.debug(f"[#808080]Couldn't get the audio source from[/#808080]: {filepath!r}")
                    logger.exception()