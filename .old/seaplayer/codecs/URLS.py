import asyncio
import hashlib
import aiofiles
import validators
# > Typing Import
from urlopen2 import URLFile
from typing import Optional
# > Local Imports
from .Any import AnyCodec
from .AnySound import AnySound

# ! Vars
SIGNATURES = {
    b'ID3': "MP3",
    b'OggS': "OGG",
    b'WAVE': "WAVE",
    b'RIFF': "WAVE"
}

# ! Any URL Sound File
class URLSoundCodec(AnyCodec):
    codec_name: str = "URLS"
    codec_priority: float=6.0
    
    # ! Codec Test
    @staticmethod
    def is_this_codec(url: str) -> bool:
        try:
            if validators.url(url):
                with URLFile(url) as file:
                    d = file.read(4)
                for i in SIGNATURES:
                    if d[:len(i)] == i:
                        return True
        except: pass
        return False
    
    @staticmethod
    async def aio_is_this_codec(url: str) -> bool:
        try:
            if validators.url(url):
                with URLFile(url) as file:
                    d = file.read(4)
                for i in SIGNATURES:
                    if d[:len(i)] == i:
                        return True
        except: pass
        return False
    
    # ! SHA1 Generation
    def __sha1__(self, buffer_size: int) -> str:
        sha1 = hashlib.sha1()
        with open(self._sound.name, "rb") as file:
            while True:
                data = file.read(buffer_size)
                if not data: break
                sha1.update(data)
        return sha1.hexdigest()
    
    async def __aio_sha1__(self, buffer_size: int) -> str:
        sha1 = hashlib.sha1()
        async with aiofiles.open(self._sound.name, "rb") as file:
            while True:
                data = await file.read(buffer_size)
                if not data: break
                sha1.update(data)
        return sha1.hexdigest()
    
    # ! Initialization
    def __init__(self, url: str, sound_device_id: Optional[int]=None, aio_init: bool=False, **kwargs) -> None:
        self.name = url
        if not aio_init:
            self._sound = AnySound.from_url(self.name, device_id=sound_device_id, **kwargs)
    
    @staticmethod
    async def __aio_init__(url: str, sound_device_id: Optional[int]=None, **kwargs):
        self = URLSoundCodec(url, aio_init=True)
        self._sound = await asyncio.to_thread(AnySound.from_url, url, device_id=sound_device_id, **kwargs)
        return self
