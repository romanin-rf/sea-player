import os
import asyncio
import aiofiles
import subprocess
from tempfile import mkstemp
# > IO's
from urlopen2 import URLFile, AsyncURLFile
# > Sound Works
from playsoundsimple import Sound
from playsoundsimple.sound import FPType, getfp
from playsoundsimple.units import DEFAULT_SOUND_FONTS_PATH
from playsoundsimple.exceptions import FileTypeError
# > Typing
from typing import Optional

# ! Vars
FLUID_SYNTH_PATH = 'fluidsynth'

# ! Main Class
class AnySound(Sound):
    @staticmethod
    async def aio_from_midi(
        fp: FPType,
        sound_fonts_path: Optional[str]=None,
        **kwargs
    ):
        path, is_temp = getfp(fp, filetype=".midi")
        sound_fonts_path = sound_fonts_path or DEFAULT_SOUND_FONTS_PATH
        if path is None:
            raise FileTypeError(fp)
        npath = mkstemp(suffix=".wav")[1]
        
        process = await asyncio.create_subprocess_exec(
            FLUID_SYNTH_PATH, "-ni", sound_fonts_path, path, "-F", npath, "-q",
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        await process.wait()
        if is_temp:
            try:
                os.remove(path)
            except:
                pass
        return AnySound(npath, **{"is_temp": True, **kwargs})
    
    @staticmethod
    def from_midi(
        fp: FPType,
        sound_fonts_path: Optional[str]=None,
        **kwargs
    ):
        path, is_temp = getfp(fp, filetype=".midi")
        sound_fonts_path = sound_fonts_path or DEFAULT_SOUND_FONTS_PATH
        if path is None:
            raise FileTypeError(fp)
        npath = mkstemp(suffix=".wav")[1]
        subprocess.call(
            [FLUID_SYNTH_PATH, "-ni", sound_fonts_path, path, "-F", npath, "-q"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        if is_temp:
            try:
                os.remove(path)
            except:
                pass
        return AnySound(npath, **{"is_temp": True, **kwargs})
    
    @staticmethod
    def from_url(url: str, **kwargs):
        path = mkstemp(suffix=".bin")[1]
        with open(path, "wb") as tempfile:
            with URLFile(url, tempfile) as urlfile:
                urlfile.fulling()
        return AnySound(path, is_temp=True, **kwargs)
    
    @staticmethod
    async def aio_from_url(url: str, **kwargs):
        path = mkstemp(suffix=".bin")[1]
        async with aiofiles.open(path, "wb") as tempfile:
            async with AsyncURLFile(url, tempfile) as urlfile:
                await urlfile.fulling()
        return AnySound(path, is_temp=True, **kwargs)
