import aiofiles
# > Local Imports
from .Any import AnyCodec


class OGGCodec(AnyCodec):
    codec_name: str = "OGG"
    codec_priority: float=3.0
    
    # ! Testing
    @staticmethod
    def is_this_codec(path: str) -> bool:
        with open(path, "rb") as file:
            return file.read(4) == b'OggS'
    
    @staticmethod
    async def aio_is_this_codec(path: str) -> bool:
        async with aiofiles.open(path, "rb") as file:
            return await file.read(4) == b'OggS'
