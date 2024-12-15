import os
import asyncio
from asyncio.queues import PriorityQueue
from uuid import uuid4, UUID
from enum import Flag, auto
from numpy import ndarray
# > Typing
from typing_extensions import Dict, Literal, Optional, Callable, NamedTuple
# > Local Imports
from ._types import SupportAudioSource, SupportAudioStreamer

# ! Constants

CHANNELS_NAMES = {
    1: 'Mono (1.0)',
    2: 'Stereo (2.0)',
    3: 'Stereo (2.1)',
    4: 'Quadro (4.0)',
    5: 'Voluminous (4.1)',
    6: 'Voluminous (5.1)',
    7: 'Voluminous (6.1)',
    8: 'Voluminous (7.1)',
    10: 'Voluminous (9.1)',
    12: 'Voluminous (10.2/11.1)',
}

# ! Track Controller State

class PlaybackerState(Flag):
    PLAYING = auto()
    PAUSED = auto()

# ! Playbacker Class

class Playbacker:
    def __init__(
        self,
        streamer: SupportAudioStreamer,
        *,
        volume: Optional[float]=None,
        piece_size: Optional[float]=None,
        tracks: Optional[Dict[UUID, 'Track']]=None,
    ) -> None:
        self.streamer = streamer
        self.tracks: Dict[UUID, 'Track'] = tracks or {}
        self.selected_track: Optional[Track] = None
        self.selected_track_uuid: Optional[UUID] = None
        self.state: PlaybackerState = PlaybackerState(0)
        self.volume: float = volume if volume is not None else 1.0
        self.piece_size: float = float(piece_size or 0.05)
        self.__running = False
    
    # ^ Propertyes
    
    @property
    def count(self) -> int:
        return len(self.tracks)
    
    @property
    def running(self) -> bool:
        return self.__running
    
    # ^ Playback Loop Methods
    
    async def __loop_pause__(self) -> None:
        while self.__running and (PlaybackerState.PAUSED in self.state) and (PlaybackerState.PLAYING in self.state):
            await asyncio.sleep(0.01)
    
    # ^ Playback Spetific Methods
    
    async def __handler_audio__(self, data: ndarray):
        return data * self.volume
    
    async def __loop__(self) -> None:
        self.__running = True
        while self.__running:
            if self.selected_track is not None:
                if PlaybackerState.PAUSED in self.state:
                    await self.__loop_pause__()
                if PlaybackerState.PLAYING in self.state:
                    if not await self.streamer.is_busy():
                        data = await self.selected_track.source.readline(self.piece_size)
                        handlered_data = await self.__handler_audio__(data)
                        await self.streamer.send(handlered_data)
            await asyncio.sleep(0.01)
    
    # ^ Playback Main Methods
    
    async def select_by_uuid(self, __uuid: UUID) -> None:
        track = self.tracks.get(__uuid, None)
        if track is not None:
            if track.uuid != self.selected_track_uuid:
                await self.stop()
                self.selected_track = track
                self.selected_track_uuid = __uuid
    
    async def select_by_track(self, __track: 'Track') -> None:
        if __track.uuid in self.tracks.keys():
            if __track.uuid != self.selected_track_uuid:
                await self.stop()
                self.selected_track = __track
                self.selected_track_uuid = __track.uuid
    
    async def select_next(self) -> UUID:
        tracks_uuids = list(self.tracks.keys())
        if len(tracks_uuids) > 0:
            selected_track_index = tracks_uuids.index(self.selected_track_uuid)
            if (selected_track_index + 1) < len(tracks_uuids):
                await self.select_by_uuid(tracks_uuids[selected_track_index + 1])
            else:
                await self.select_by_uuid(tracks_uuids[0])
    
    async def play(self) -> None:
        if PlaybackerState.PLAYING not in self.state:
            self.state |= PlaybackerState.PLAYING
            # TODO: Нужно как-то сделать вызов события начала воспроизведения
    
    async def stop(self) -> None:
        if PlaybackerState.PLAYING in self.state:
            self.state &= ~PlaybackerState.PLAYING
            await self.streamer.abort()
            if self.selected_track is not None:
                await self.selected_track.set_position(0)
            # TODO: Нужно как-то сделать вызов события остановки воспроизведения
    
    async def pause(self) -> None:
        if PlaybackerState.PAUSED not in self.state:
            self.state |= PlaybackerState.PAUSED
            # TODO: Нужно как-то сделать вызов события паузы
    
    async def unpause(self) -> None:
        if PlaybackerState.PAUSED in self.state:
            self.state &= ~PlaybackerState.PAUSED
            # TODO: Нужно как-то сделать вызов события снятия с паузы

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
    
    def __str__(self) -> str:
        return f"(<{self.__class__.__name__}> with {self.source!r})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
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
                return PlaybackerState.PLAYING in self.playbacker.state
        return False
    
    @property
    def paused(self) -> bool:
        if self.playbacker.selected_track is not None:
            if self.playbacker.selected_track_uuid == self.uuid:
                return PlaybackerState.PAUSED in self.playbacker.state
        return False
    
    @property
    def selected(self) -> bool:
        if self.playbacker.selected_track is not None:
            return self.playbacker.selected_track_uuid == self.uuid
        return False
    
    @property
    def frames(self) -> int:
        return self.source.sfio.frames
    
    @property
    def duration(self) -> float:
        return self.source.sfio.frames / self.source.samplerate
    
    @property
    def cover(self):
        return self.source.metadata.icon
    
    # ^ Playback Methods
    
    def __playback_name__(self) -> str:
        if self.metadata.artist is not None:
            if self.metadata.title is not None:
                return f"{self.metadata.artist} - {self.metadata.title}"
            title = os.path.splitext(self.source.name)[0]
            return f"{self.metadata.artist} - {title}"
        return os.path.splitext(self.source.name)[0]
    
    def __playback_subtitle__(self) -> str:
        attrs = []
        attrs.append(f'{self.source.samplerate} Hz')
        if self.source.channels > 0:
            attrs.append(CHANNELS_NAMES.get(self.source.channels, f'{self.source.channels} channels'))
        attrs.append(f'{round(self.source.bitrate / 1000)} kbps')
        attrs.append(self.source.format)
        return ', '.join(attrs)
    
    # ^ Track Methods
    
    async def get_position(self) -> float:
        return (await self.source.tell()) / self.source.samplerate
    
    async def set_position(self, __position: float) -> None:
        new_position = round(__position * self.source.samplerate)
        await self.source.seek(new_position)
    
    async def play(self) -> None:
        if self.playbacker.selected_track_uuid == self.uuid:
            await self.playbacker.play()
    
    async def stop(self) -> None:
        if self.playbacker.selected_track_uuid == self.uuid:
            await self.playbacker.stop()
    
    async def pause(self) -> None:
        if self.playbacker.selected_track_uuid == self.uuid:
            await self.playbacker.pause()
    
    async def unpause(self) -> None:
        if self.playbacker.selected_track_uuid == self.uuid:
            await self.playbacker.unpause()
    
    async def get_volume(self) -> float:
        return self.playbacker.volume
    
    async def set_volume(self, __volume: float) -> None:
        if self.playbacker.selected_track_uuid == self.uuid:
            if __volume >= 0:
                self.playbacker.volume = float(__volume)
    
    async def select(self) -> None:
        await self.playbacker.select_by_track(self)