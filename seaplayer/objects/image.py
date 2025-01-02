import asyncio
from enum import IntEnum
from textual.widgets import Label
from rich.console import RenderableType
from PIL.Image import Image, Resampling
# > Typing
from typing_extensions import (
    Tuple,
)
# > Local Imports
from seaplayer.others.ripix import RichPixels, HalfcellRenderer, FullcellRenderer

# ! Types

class RenderMode(IntEnum):
    NONE = 0
    FULL = 1
    HALF = 2

# ! Main Class
class ImageWidget(Label):
    DEFAULT_CSS = """
    ImageWidget {
        height: 1fr;
        width: 1fr;
        align: center middle;
        text-align: center;
    }
    """
    
    @staticmethod
    def image2pixels(
        image: Image,
        resize: Tuple[int, int] | None = None,
        resample: Resampling | None = None,
        render_mode: RenderMode | None = None
    ) -> RichPixels:
        render_mode = render_mode if render_mode is not None else RenderMode.NONE
        match render_mode:
            case RenderMode.NONE:
                return RichPixels.from_image(image, resize, resample)
            case RenderMode.FULL:
                return RichPixels.from_segments(FullcellRenderer().render(image, resize, resample))
            case RenderMode.HALF:
                return RichPixels.from_segments(HalfcellRenderer().render(image, resize, resample))
        raise ValueError(f'{render_mode=!r}')
    
    def __init__(
        self,
        default: Image | RenderableType | None = None,
        image: Image | None = None,
        resample: Resampling | None = None,
        render_mode: RenderMode | None = None,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False
    ) -> None:
        self.__default = default or "<image not found>"
        self.__image = image
        self.__resample = resample if resample is not None else Resampling.NEAREST
        self.__render_mode = render_mode if render_mode is not None else RenderMode.HALF
        self.__last_image_size = None
        if image is None:
            if isinstance(self.__default, Image):
                self.__content = self.image2pixels(
                    self.__default, 
                    resample=Resampling.NEAREST,
                    render_mode=self.__render_mode
                )
            else:
                self.__content = self.__default
        else:
            self.__content = self.image2pixels(
                self.__image,
                resample=self.__resample,
                render_mode=self.__render_mode
            )
        super().__init__(self.__content, name=name, id=id, classes=classes, disabled=disabled)
    
    async def on_resize(self):
        size = (self.container_viewport.size[0], self.container_viewport.size[1])
        if self.__last_image_size != size:
            await self.refresh_image(size)
    
    async def update_image(self, image: Image | None = None) -> None:
        self.__image = image
        await self.refresh_image()
        self.update(self.__content)
    
    async def refresh_image(self, size: Tuple[int, int] | None = None) -> None:
        if size is None:
            size = (self.container_viewport.size[0], self.container_viewport.size[1])
        if self.__image is not None:
            self.__content = await asyncio.to_thread(
                self.image2pixels, self.__image, size, self.__resample, self.__render_mode
            )
            self.__last_image_size = size
        else:
            if isinstance(self.__default, Image):
                self.__content = await asyncio.to_thread(
                    self.image2pixels, self.__default, size, Resampling.NEAREST, self.__render_mode
                )
            else:
                self.__content = self.__default
            self.__last_image_size = size
        self.update(self.__content)
