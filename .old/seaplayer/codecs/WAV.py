import aiofiles
# > Local Imports
from .Any import AnyCodec


class WAVECodec(AnyCodec):
    codec_name: str = "WAVE"
    codec_priority: float=2.0
    
    # ! Testing
    @staticmethod
    def is_this_codec(path: str) -> bool:
        with open(path, "rb") as file:
            signature = file.read(4)
        return (signature == b'WAVE') or (signature == b'RIFF')
    
    @staticmethod
    async def aio_is_this_codec(path: str) -> bool:
        async with aiofiles.open(path, "rb") as file:
            signature = await file.read(4)
        return (signature == b'WAVE') or (signature == b'RIFF')