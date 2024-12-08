from .MP3 import MP3Codec
from .OGG import OGGCodec
from .WAV import WAVECodec
from .MIDI import MIDICodec
from .FLAC import FLACCodec
from .URLS import URLSoundCodec
from .Any import AnyCodec
from ..codeсbase import CodecBase
from typing import List

codecs: List[CodecBase] = [ MP3Codec, OGGCodec, WAVECodec, MIDICodec, FLACCodec, URLSoundCodec, AnyCodec ]
