"""
It is a cut-out part of the code from the `rich_pixels` project.
"""


from __future__ import annotations


from pathlib import Path, PurePath
# > Pillow
from PIL import Image as PILImageModule
from PIL.Image import Image
from PIL.Image import Resampling
# > Rich
from rich.console import Console, ConsoleOptions, RenderResult
from rich.segment import Segment, Segments
from rich.style import Style
# > Typing
from typing_extensions import (
    Tuple, List,
    Iterable, Mapping,
    Union, Optional,
    Self
)


class RichPixels:
    def __init__(self) -> None:
        self._segments: Optional[Segments] = None
    
    @staticmethod
    def from_image(
        image: Image,
        resize: Optional[Tuple[int, int]]=None,
        resample: Optional[Resampling]=None
    ) -> RichPixels:
        resample = resample or Resampling.NEAREST
        segments = RichPixels._segments_from_image(image, resize, resample)
        return RichPixels.from_segments(segments)
    
    @staticmethod
    def from_image_path(
        path: Union[PurePath, str],
        resize: Optional[Tuple[int, int]]=None,
        resample: Optional[Resampling]=None
    ) -> RichPixels:
        """Create a *RichPixels* object from an image. Requires 'image' extra dependencies.
        
        Args:
            path: The path to the image file.
            resize: A tuple of (width, height) to resize the image to.
        """
        resample = resample or Resampling.NEAREST
        with PILImageModule.open(Path(path)) as image:
            segments = RichPixels._segments_from_image(image, resize, resample)
        return RichPixels.from_segments(segments)
    
    @staticmethod
    def _segments_from_image(
        image: Image,
        resize: Optional[Tuple[int, int]]=None,
        resample: Optional[Resampling]=None
    ) -> List[Segment]:
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        if resize is not None:
            image = image.resize(resize, resample)
        height, width = image.size
        null_style = Style.null()
        segments = []
        for y in range(width):
            this_row = []
            for x in range(height):
                r, g, b, a = image.getpixel((x, y))
                if a > 0:
                    style = Style.parse(f"on rgb({r},{g},{b})")
                else:
                    style = null_style
                this_row.append(Segment(" ", style))
            this_row.append(Segment("\n", null_style))
            segments += this_row
        return segments
    
    @staticmethod
    def from_segments(
        segments: Iterable[Segment],
    ) -> Self:
        """Create a Pixels object from an Iterable of Segments instance.

        Args:
            segments (Iterable[Segment]): Image segments.
        """
        pixels = RichPixels()
        pixels._segments = Segments(segments)
        return pixels
    
    @staticmethod
    def from_ascii(
        grid: str,
        mapping: Optional[Mapping[str, Segment]]=None
    ) -> Self:
        """
        Create a Pixels object from a 2D-grid of ASCII characters.
        Each ASCII character can be mapped to a Segment (a character and style combo),
        allowing you to add a splash of colour to your grid.
        
        Args:
            grid: A 2D grid of characters (a multi-line string).
            mapping: Maps ASCII characters to Segments. Occurrences of a character will be replaced with the corresponding Segment.
        """
        if mapping is None:
            mapping = {}
        if not grid:
            return RichPixels.from_segments([])
        segments = []
        for character in grid:
            segment = mapping.get(character, Segment(character))
            segments.append(segment)
        return RichPixels.from_segments(segments)
    
    def __rich_console__(
        self,
        console: Console,
        options: ConsoleOptions
    ) -> RenderResult:
        yield self._segments or ""
