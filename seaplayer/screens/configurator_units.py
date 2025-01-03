import sounddevice as sd
from enum import Flag, auto
# > Typing
from typing_extensions import (
    Tuple, List,
    Iterator, Iterable, TypedDict,
    TypeAlias
)
# > Local Imports
from seaplayer.units import ll

# ! Types

class ConfigurateState(Flag):
    LANGUAGE = auto()
    DEVICE_ID = auto()
    IMAGE_RESAMPLING = auto()
    IMAGE_RENDER_MODE = auto()
    LOG_LEVEL = auto()

# ! Types Alias

class DeviceInfo(TypedDict):
    name: str
    index: int
    hostapi: int
    max_input_channels: int
    max_output_channels: int
    default_low_input_latency: float
    default_low_output_latency: float
    default_high_input_latency: float
    default_high_output_latency: float
    default_samplerate: float

class HostAPIInfo(TypedDict):
    name: str
    devices: List[int]
    default_input_device: int
    default_output_device: int

DevicesInfo: TypeAlias = Iterable[DeviceInfo]
HostAPIsInfo: TypeAlias = Tuple[HostAPIInfo]

# ! Methods

def _rr(_: bool):
    if _:
        return ' [red]\\[%s][/red]' % ll.get('words.restart_required')
    return ''

# ! Spetific Methods

def query_sounddevices() -> Iterator[Tuple[int, str, str]]:
    hosts: HostAPIsInfo = sd.query_hostapis()
    devices: DevicesInfo = sd.query_devices()
    for device in filter(lambda i: i.get('max_output_channels', 0) > 0, devices):
        yield device['index'], device['name'], hosts[device['hostapi']]['name']

# ! Annotations

__all__ = [
    'ConfiguratorState',
    'DeviceInfo', 'HostAPIInfo', 'DevicesInfo', 'HostAPIsInfo',
    '_rr', 'query_sounddevices'
]