import asyncio
from vkpymusic import Service, Song
from seaplayer.codecs.URLS import URLSoundCodec
from seaplayer.codecs.AnySound import AnySound
# > Typing
from typing import Optional, List
# > Local Imports
from .units import (
    pget,
    pchecks,
    VKM_SUID_PATTERN,
    VKM_TEXT_RANGE_OFFSET_PATTERN
)

# ! Methods
def get_song(service: Service, value: str) -> Optional[Song]:
    songs: List[Song] = []
    # ! "vkm://by/users?uid=<uid:int>&sid=<sid:int>"
    if (d:=pget(VKM_SUID_PATTERN, value)) is not None:
        songs += service.get_songs_by_userid(d['uid'], 1, d['sid'])
    # ! "vkm://by/text?t=<text>&c=<count:int>&o=<offset:int>"
    elif (d:=pget(VKM_TEXT_RANGE_OFFSET_PATTERN, value)) is not None:
        songs += service.search_songs_by_text(d['text'], d['count'], d['offset'])
    return songs[0] if len(songs) > 0 else None

# ! Main Class
class VKMCodec(URLSoundCodec):
    codec_name = "VKM"
    codec_priority = 5.999
    hidden_name = True
    
    # ! Check Methods
    @staticmethod
    def is_this_codec(value: str) -> bool:
        return pchecks(value, VKM_SUID_PATTERN, VKM_TEXT_RANGE_OFFSET_PATTERN)
    
    @staticmethod
    async def aio_is_this_codec(value: str) -> bool:
        return pchecks(value, VKM_SUID_PATTERN, VKM_TEXT_RANGE_OFFSET_PATTERN)
    
    # ! Main Functions
    def __init__(
        self,
        url: str,
        vkm_service: Optional[Service]=None,
        sound_device_id: Optional[int]=None,
        aio_init: bool=False,
        **kwargs
    ) -> None:
        if vkm_service is None:
            raise RuntimeError("The VKM service has not been initialized.")
        self.song = get_song(vkm_service, url)
        if self.song is None:
            raise RuntimeError("The sound could not be retrieved.")
        self._title = (self.song.title if (len(self.song.title) > 0) else None) if isinstance(self.song.title, str) else None
        self._artist = (self.song.artist if (len(self.song.artist) > 0) else None) if isinstance(self.song.artist, str) else None
        super().__init__(self.song.url, sound_device_id, aio_init, **kwargs)
        self.name = ""
    
    @staticmethod
    async def __aio_init__(
        url: str,
        sound_device_id: Optional[int]=None,
        vkm_service: Optional[Service]=None,
        **kwargs
    ):
        self = VKMCodec(url, vkm_service=vkm_service, sound_device_id=sound_device_id, aio_init=True)
        self._sound = await asyncio.to_thread(AnySound.from_url, self.song.url, device_id=sound_device_id, **kwargs)
        return self
    
    # ! Properys
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def artist(self) -> str:
        return self._artist