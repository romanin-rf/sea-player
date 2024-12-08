import os
import aiofiles
# > Typing Import
from typing import Optional
# > Local Imports
from .Any import AnyCodec
from .AnySound import AnySound

# ! Codec
class MIDICodec(AnyCodec):
    codec_name: str = "MIDI"
    codec_priority: float=5.0
    
    # ! Testing
    @staticmethod
    def is_this_codec(path: str) -> bool:
        with open(path, 'rb') as file:
            return file.read(4) == b"MThd"
    
    @staticmethod
    async def aio_is_this_codec(path: str) -> bool:
        async with aiofiles.open(path, 'rb') as file:
            return await file.read(4) == b"MThd"
    
    # ! Initialized
    def __init__(self, path: str, aio_init: bool=False, sound_device_id: Optional[int]=None, **kwargs) -> None:
        self.name = os.path.abspath(path)
        if not aio_init:
            self._sound = AnySound.from_midi(self.name, device_id=sound_device_id, **kwargs)
    
    @staticmethod
    async def __aio_init__(path: str, sound_device_id: Optional[int]=None, **kwargs):
        self = MIDICodec(path, aio_init=True)
        self._sound = await AnySound.aio_from_midi(self.name, device_id=sound_device_id, **kwargs)
        return self
