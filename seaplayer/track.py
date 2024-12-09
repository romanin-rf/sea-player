from uuid import uuid4, UUID
from enum import Flag, auto
# > Typing
from typing_extensions import Dict, Literal, Optional, Callable
# > Local Imports
from ._types import SupportAudioSource, SupportAudioStreamer

# ! Track Controller State

class PlaybackerState(Flag):
    PLAYING = auto()
    PAUSED = auto()

# ! Playbacker Class

class Playbacker:
    def __init__(
        self,
        streamer: SupportAudioStreamer,
        volume: Optional[float]=None,
        piece_size: Optional[float]=None,
        tracks: Optional[Dict[UUID, 'Track']]=None,
        callback: Optional[ Callable[[Literal['add', 'remove', 'select'], 'Track'], None] ]=None
    ) -> None:
        self.streamer = streamer
        self.tracks: Dict[UUID, 'Track'] = tracks or {}
        self.selected_track: Optional[Track] = None
        self.selected_track_uuid: Optional[UUID] = None
        self.state: PlaybackerState = PlaybackerState(0)
        self.volume: float = float(volume or 1.0)
        self.piece_size: float = float(piece_size or 0.1)
        self.callback = callback
        self.__running = False
    
    # ^ Propertyes
    
    @property
    def count(self) -> int:
        return len(self.tracks)
    
    @property
    def running(self) -> bool:
        return self.__running
    
    # ^ Playback Methods
    
    async def __loop__(self) -> None:
        self.__running = True
        while self.__running:
            pass
    
    async def select_by_uuid(self, __uuid: UUID) -> None:
        pass
    
    async def select_by_track(self, __track: 'Track') -> None:
        pass
    
    async def play(self) -> None:
        pass
    
    async def stop(self) -> None:
        pass

    # ^ Playlist Methods
    
    def add(self, __track: 'Track') -> UUID:
        self.tracks[__uuid := uuid4()] = __track
        return __uuid
    
    def remove(self, __uuid: UUID) -> bool:
        track = self.tracks.pop(__uuid, None)
        if track is not None:
            del track

# ! Track Class

class Track:
    def __init__(
        self,
        source: SupportAudioSource,
        playbacker: Playbacker
    ) -> None:
        self.source = source
        self.playbacker = playbacker
        self.__uuid = self.playbacker.add(self)
    
    # ^ Dander Methods
    
    def __del__(self) -> None:
        del self.source
    
    # ^ Propertyes
    
    @property
    def uuid(self) -> UUID:
        return self.__uuid
    
    @property
    def metadata(self):
        return self.source.metadata
    
    @property
    def playing(self) -> bool:
        if self.playbacker.selected_track is not None:
            if self.playbacker.selected_track_uuid == self.uuid:
                return PlayerState.PLAYING in self.playbacker.state
        return False
    
    @property
    def paused(self) -> bool:
        if self.playbacker.selected_track is not None:
            if self.playbacker.selected_track_uuid == self.uuid:
                return PlayerState.PAUSED in self.playbacker.state
        return False
    
    @property
    def selected(self) -> bool:
        if self.playbacker.selected_track is not None:
            return self.playbacker.selected_track_uuid == self.uuid
        return False
    
    @property
    def duration(self) -> float:
        return self.source.sfio.frames / self.source.samplerate
    
    # ^ Track Methods
    
    async def get_position(self) -> float:
        return (await self.source.tell()) / self.source.samplerate
    
    async def set_position(self, __position: float) -> None:
        new_position = round(__position * self.source.samplerate)
        await self.source.seek(new_position)
    
    async def play(self) -> None:
        pass
    
    async def stop(self) -> None:
        pass
    
    async def pause(self) -> None:
        pass
    
    async def get_volume(self) -> float:
        return self.playbacker.volume
    
    async def set_volume(self, __volume: float) -> None:
        self.playbacker.volume = float(__volume)