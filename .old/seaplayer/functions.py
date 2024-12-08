import os
import asyncio
import aiofiles
from io import BytesIO
# > Image Works
from PIL import Image
# > Typing
from typing_extensions import (
    deprecated,
    TypeVar,
    Coroutine,
    Awaitable,
    Callable,
    AsyncGenerator,
    Literal,
    Optional,
    Iterable,
    Union,
    Tuple,
    Any
)
# > Local Imports
from .codeсbase import CodecBase

# ! Types Vars
T = TypeVar("T")
RT = TypeVar("RT")

# ! Async Functions
async def aiter(it: Iterable[T]) -> AsyncGenerator[T, Any]:
    for i in it:
        await asyncio.sleep(0)
        yield i

async def get_bar_status() -> Tuple[str, Optional[float], Optional[float]]:
    return "", None, None

async def aio_is_midi_file(filepath: str):
    async with aiofiles.open(filepath, 'rb') as file:
        return await file.read(4) == b"MThd"

async def aio_check_status_code(sound: CodecBase) -> Literal[0, 1, 2]:
    if sound.playing:
        return 2 if sound.paused else 1
    else:
        return 0

# ! Exceptions Rich
def rich_exception(exc: Exception) -> str:
    return f"[red]{exc.__class__.__name__}[/red]: {exc.__str__()}"

# ! Functions
def formater(**kwargs) -> str:
    return ", ".join([f"{key}={repr(value)}" for key, value in kwargs.items()])

@deprecated("Use `seaplayer.seaplayer.SeaPlayer.get_sound_tstatus`.")
def check_status(sound: CodecBase) -> Literal["Stoped", "Playing", "Paused"]:
    if sound.playing:
        if sound.paused:
            return "Paused"
        else:
            return "Playing"
    return "Stoped"

def get_sound_basename(sound: CodecBase) -> str:
    if sound.title is not None:
        if sound.artist is not None:
            return f"{sound.artist} - {sound.title}"
        return f"{sound.title}"
    if sound.name is not None:
        try:
            return f"{os.path.basename(sound.name)}"
        except:
            return sound.name
    else:
        return "<memory>"

def image_from_bytes(data: Optional[bytes]) -> Optional[Image.Image]:
    if data is not None:
        return Image.open(BytesIO(data))

# ! Wrappers
def awrap(
    method: Union[
        Callable[..., Awaitable[RT]], 
        Callable[..., Coroutine[Any, Any, RT]]
    ],
    *args, **kwargs
) -> Callable[[], Coroutine[Any, Any, RT]]:
    async def wrapped():
        return await method(*args, **kwargs)
    return wrapped