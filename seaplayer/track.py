from uuid import uuid4, UUID
from enum import Flag, auto
# > Typing
from typing_extensions import Dict, Optional
# > Local Imports
from ._types import SupportAudioSource, SupportAudioStreamer

# ! Track Controller State

class TracksControllerState(Flag):
    PLAYING = auto()
    PAUSED = auto()

# ! Track Contoller Class

class TracksController:
    def __init__(self, streamer: SupportAudioStreamer) -> None:
        self.streamer = streamer
        self.tracks: Dict[UUID, Track] = {}
        self.current_track: Optional[Track] = None
        self.current_track_uuid: Optional[UUID] = None
        self.state = TracksControllerState(0)
    
    def add(self, __track: 'Track') -> UUID:
        self.tracks[__uuid := uuid4()] = __track
        return __uuid
    
    def select(self, __uuid: UUID) -> None:
        track = self.tracks.get(__uuid, None)
        if track is not None:
            # TODO: if track.playing:
            # TODO:     self.current_track.stop()
            self.current_track = track
            self.current_track_uuid = track.uuid
    
    def play(self, __uuid: UUID) -> None:
        pass
    
    def stop(self, __uuid: UUID) -> None:
        pass
    
    def pause(self, __uuid: UUID) -> None:
        pass

# ! Track Class

class Track:
    def __init__(
        self,
        source: SupportAudioSource,
        controller: TracksController
    ) -> None:
        self.source = source
        self.controller = controller
        
        self.__uuid = self.controller.add(self)
    
    @property
    def uuid(self) -> UUID:
        return self.__uuid