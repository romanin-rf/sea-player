"""
It is a cut-out part of the code from the `rich_pixels` project.

Repository: https://github.com/darrenburns/rich-pixels
"""


from __future__ import annotations


from pathlib import Path
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
    Callable,
)
# > Local Imports
from seaplayer._types import FilePathType

# ! Types

RGBA = Tuple[int, int, int, int]
GetPixel = Callable[[Tuple[int, int]], RGBA]

# ! Methods

def _get_color(pixel: RGBA, default_color: str | None = None) -> str | None:
    r, g, b, a = pixel
    return f"rgb({r},{g},{b})" if a > 0 else default_color

# ! Render Base Class

class Renderer:
    """
    Base class for renderers.
    """

    default_color: str | None
    null_style: Style | None

    def __init__(
        self,
        *,
        default_color: str | None = None,
    ) -> None:
        self.default_color = default_color
        self.null_style = (
            None if default_color is None else Style.parse(f"on {default_color}")
        )

    def render(self, image: Image, resize: Tuple[int, int] | None, resample: Resampling | None = None) -> List[Segment]:
        """
        Render an image to Segments.
        """
        resample = resample or Resampling.NEAREST
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        if resize is not None:
            image = image.resize(resize, resample=resample)

        get_pixel = image.getpixel
        width, height = image.width, image.height

        segments = []

        for y in self._get_range(height):
            this_row: List[Segment] = []

            this_row += self._render_line(
                line_index=y, width=width, get_pixel=get_pixel
            )
            this_row.append(Segment("\n", self.null_style))

            # TODO: Double-check if this is required - I've forgotten...
            if not all(t[1] == "" for t in this_row[:-1]):
                segments += this_row

        return segments

    def _get_range(self, height: int) -> range:
        """
        Get the range of lines to render.
        """
        raise NotImplementedError

    def _render_line(
        self, *, line_index: int, width: int, get_pixel: GetPixel
    ) -> List[Segment]:
        """
        Render a line of pixels.
        """
        raise NotImplementedError

# ! Render Classes

class HalfcellRenderer(Renderer):
    """
    Render an image to half-height cells.
    """

    def render(self, image: Image, resize: Tuple[int, int] | None, resample: Resampling | None = None) -> List[Segment]:
        """
        Because each row is 2 lines high, so we need to make sure the height is even
        """
        
        resample = resample or Resampling.NEAREST
        
        target_height = (resize[1] * 2) if (resize is not None) else (image.size[1] * 2)
        if target_height % 2 != 0:
            target_height += 1

        if image.size[1] != target_height:
            resize = (
                (resize[0], target_height) if (resize is not None) else (image.size[0], target_height)
            )

        return super().render(image, resize, resample)

    def _get_range(self, height: int) -> range:
        return range(0, height, 2)

    def _render_line(
        self, *, line_index: int, width: int, get_pixel: GetPixel
    ) -> List[Segment]:
        line = []
        for x in range(width):
            line.append(self._render_halfcell(x=x, y=line_index, get_pixel=get_pixel))
        return line

    def _render_halfcell(self, *, x: int, y: int, get_pixel: GetPixel) -> Segment:
        colors = []

        # get lower pixel, render lower pixel use foreground color, so it must be first
        lower_color = _get_color(
            get_pixel((x, y + 1)), default_color=self.default_color
        )
        colors.append(lower_color or "")
        # get upper pixel, render upper pixel use background color, it is optional
        upper_color = _get_color(get_pixel((x, y)), default_color=self.default_color)
        if upper_color:
            colors.append(upper_color or "")

        style = Style.parse(" on ".join(colors)) if colors else self.null_style
        # use lower halfheight block to render if lower pixel is not transparent
        return Segment('▄' if lower_color else ' ', style)


class FullcellRenderer(Renderer):
    """
    Render an image to full-height cells.
    """

    def _get_range(self, height: int) -> range:
        return range(height)

    def _render_line(
        self, *, line_index: int, width: int, get_pixel: GetPixel
    ) -> List[Segment]:
        line = []
        for x in range(width):
            line.append(self._render_fullcell(x=x, y=line_index, get_pixel=get_pixel))
        return line

    def _render_fullcell(self, *, x: int, y: int, get_pixel: GetPixel) -> Segment:
        pixel = get_pixel((x, y))
        style = (
            Style.parse(f"on {_get_color(pixel, default_color=self.default_color)}")
            if pixel[3] > 0
            else self.null_style
        )
        return Segment("  ", style)
    
    def render(self, image: Image, resize: Tuple[int, int] | None, resample: Resampling | None = None) -> List[Segment]:
        """
        Render an image to Segments.
        """
        resample = resample or Resampling.NEAREST
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        if resize is not None:
            resize = (int(resize[0] // 2), resize[1])
            image = image.resize(resize, resample=resample)

        get_pixel = image.getpixel
        width, height = image.width, image.height

        segments = []

        for y in self._get_range(height):
            this_row: List[Segment] = []

            this_row += self._render_line(
                line_index=y, width=width, get_pixel=get_pixel
            )
            this_row.append(Segment("\n", self.null_style))

            if not all(t[1] == "" for t in this_row[:-1]):
                segments += this_row

        return segments

# ! Pixels Container Class

class RichPixels:
    def __init__(self) -> None:
        self._segments: Segments | None = None
    
    @staticmethod
    def from_image(
        image: Image,
        resize: Tuple[int, int] | None = None,
        resample: Resampling | None = None
    ) -> RichPixels:
        resample = resample or Resampling.NEAREST
        segments = RichPixels._segments_from_image(image, resize, resample)
        return RichPixels.from_segments(segments)
    
    @staticmethod
    def from_image_path(
        path: FilePathType,
        resize: Tuple[int, int] | None = None,
        resample: Resampling | None = None
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
        resize: Tuple[int, int] | None = None,
        resample: Resampling | None = None
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
    ) -> RichPixels:
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
        mapping: Mapping[str, Segment] | None = None
    ) -> RichPixels:
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
