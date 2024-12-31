import asyncio
from enum import IntEnum
from PIL.Image import Image, Resampling
from textual.widgets import Label
from rich.console import RenderableType
# > Local Imports
from ..others.ripix import RichPixels, HalfcellRenderer, FullcellRenderer
# > Typing
from typing_extensions import (
    Tuple,
    Union, Optional,
)

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
        resize: Optional[Tuple[int, int]]=None,
        resample: Optional[Resampling]=None,
        render_mode: Optional[RenderMode]=None
    ) -> RichPixels:
        render_mode = render_mode or RenderMode.NONE
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
        default: Optional[Union[Image, RenderableType]]=None,
        image: Optional[Image]=None,
        resample: Optional[Resampling]=None,
        render_mode: Optional[RenderMode]=None
    ) -> None:
        self.__default = default or "<image not found>"
        self.__image = image
        self.__resample = resample or Resampling.NEAREST
        self.__render_mode = render_mode or RenderMode.HALF
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
        super().__init__(self.__content)
    
    async def on_resize(self):
        size = (self.container_viewport.size[0], self.container_viewport.size[1])
        if self.__last_image_size != size:
            await self.refresh_image(size)
    
    async def update_image(self, image: Optional[Image]=None) -> None:
        self.__image = image
        await self.refresh_image()
        self.update(self.__content)
    
    async def refresh_image(self, size: Optional[Tuple[int, int]]=None) -> None:
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