import os
import datetime
from numpy import ndarray
from enum import Flag, auto
from uuid import uuid4, UUID
from textual.app import App
from textual.message import Message
from seaplayer_audio import CallbackSoundDeviceStreamer
# > Typing
from typing_extensions import Dict, Optional
# > Local Imports
from .others.cache import Cacher
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

def formtime() -> str:
    return '{0.day:0>2}.{0.month:0>2}.{0.year:0>4} {0.hour:0>2}:{0.minute:0>2}:{0.second:0>2}.{0.microsecond}'.format(
        datetime.datetime.now()
    )

# ! Track Controller State

class PlaybackerState(Flag):
    PLAYING = auto()
    PAUSED = auto()

# ! Messages

class PlaybackerChangeStateMessage(Message):
    def __init__(self) -> None:
        super().__init__()

# ! Playbacker Class

class Playbacker:
    def __init__(
        self,
        app: App,
        *,
        volume: Optional[float]=None,
        tracks: Optional[Dict[UUID, 'Track']]=None,
    ) -> None:
        self.app: App = app
        self.cacher: Cacher = self.app.cacher
        self.streamer: SupportAudioStreamer = CallbackSoundDeviceStreamer(precallback=self.__loop_frame__)
        self.tracks: Dict[UUID, 'Track'] = tracks or {}
        self.selected_track: Optional[Track] = None
        self.selected_track_uuid: Optional[UUID] = None
        self.state: PlaybackerState = PlaybackerState(0)
        self.volume: float = volume or 1.0
        self.__running = False
    
    # ^ Propertyes
    
    @property
    def count(self) -> int:
        return len(self.tracks)
    
    @property
    def running(self) -> bool:
        return self.__running
    
    @running.setter
    def running(self, value: bool) -> None:
        self.__running = value
    
    # ^ Playback Spetific Methods
    
    def __handler_audio__(self, data: ndarray):
        return data * self.volume
    
    def __loop_frame__(self, frames: int) -> None:
        if (self.selected_track is not None) and (PlaybackerState.PLAYING in self.state) and (PlaybackerState.PAUSED not in self.state):
            data = self.selected_track.source.read(frames)
            if len(data) == 0:
                self.stop()
                return
            self.streamer.send(self.__handler_audio__(data))
    
    # ^ Playbacker Methods
    
    def start(self) -> None:
        if not self.__running:
            self.running = True
            self.streamer.start()
    
    def terminate(self) -> None:
        if self.__running:
            self.running = False
            self.streamer.stop()
    
    # ^ Playback Main Methods
    
    def select_by_uuid(self, __uuid: UUID) -> None:
        track = self.tracks.get(__uuid, None)
        if track is not None:
            if track.uuid != self.selected_track_uuid:
                self.stop()
                self.selected_track = track
                self.selected_track_uuid = __uuid
    
    def select_by_track(self, __track: 'Track') -> None:
        if __track.uuid in self.tracks.keys():
            if __track.uuid != self.selected_track_uuid:
                self.stop()
                self.selected_track = __track
                self.selected_track_uuid = __track.uuid
    
    def select_next(self) -> UUID:
        tracks_uuids = list(self.tracks.keys())
        if len(tracks_uuids) > 0:
            selected_track_index = tracks_uuids.index(self.selected_track_uuid)
            if (selected_track_index + 1) < len(tracks_uuids):
                self.select_by_uuid(tracks_uuids[selected_track_index + 1])
            else:
                self.select_by_uuid(tracks_uuids[0])
    
    def play(self) -> None:
        if PlaybackerState.PLAYING not in self.state:
            self.state |= PlaybackerState.PLAYING
            self.app.post_message(PlaybackerChangeStateMessage())
    
    def stop(self) -> None:
        if PlaybackerState.PLAYING in self.state:
            self.state = PlaybackerState(0)
            if self.selected_track is not None:
                self.selected_track.set_position(0)
            self.app.post_message(PlaybackerChangeStateMessage())
    
    def pause(self) -> None:
        if PlaybackerState.PAUSED not in self.state:
            self.state |= PlaybackerState.PAUSED
            self.app.post_message(PlaybackerChangeStateMessage())
    
    def unpause(self) -> None:
        if PlaybackerState.PAUSED in self.state:
            self.state &= ~PlaybackerState.PAUSED
            self.app.post_message(PlaybackerChangeStateMessage())
    
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
    
    def get_position(self) -> float:
        return (self.source.tell()) / self.source.samplerate
    
    def set_position(self, __position: float) -> None:
        new_position = round(__position * self.source.samplerate)
        self.source.seek(new_position)
    
    def play(self) -> None:
        if self.playbacker.selected_track_uuid == self.uuid:
            self.playbacker.play()
    
    def stop(self) -> None:
        if self.playbacker.selected_track_uuid == self.uuid:
            self.playbacker.stop()
    
    def pause(self) -> None:
        if self.playbacker.selected_track_uuid == self.uuid:
            self.playbacker.pause()
    
    def unpause(self) -> None:
        if self.playbacker.selected_track_uuid == self.uuid:
            self.playbacker.unpause()
    
    def get_volume(self) -> float:
        return self.playbacker.volume
    
    def set_volume(self, __volume: float) -> None:
        if self.playbacker.selected_track_uuid == self.uuid:
            if __volume >= 0:
                self.playbacker.volume = float(__volume)
    
    def select(self) -> None:
        self.playbacker.select_by_track(self)