import asyncio
from PIL.Image import Image, Resampling
from textual.widgets import Label
from rich.console import RenderableType
# > Local Imports
from ..others.ripix import RichPixels
# > Typing
from typing_extensions import Union, Optional, Tuple

# ! Main Class
class ImageWidget(Label):
    DEFAULT_CSS = """
    StandartImageLabel {
        height: 1fr;
        width: 1fr;
        align: center middle;
        text-align: center;
    }
    """
    
    @staticmethod
    def image2pixels(
        __image: Image,
        __resize: Optional[Tuple[int, int]]=None,
        __resample: Optional[Resampling]=None
    ) -> RichPixels:
        return RichPixels.from_image(__image, __resize, __resample)
    
    def __init__(
        self,
        default: Optional[Union[Image, RenderableType]]=None,
        image: Optional[Image]=None,
        resample: Optional[Resampling]=None
    ) -> None:
        self.__default = default or "<image not found>"
        self.__image = image
        self.__resample = resample or Resampling.NEAREST
        self.__last_image_size = None
        if image is None:
            if isinstance(self.__default, Image):
                self.__content = self.image2pixels(self.__default)
            else:
                self.__content = self.__default
        else:
            self.__content = self.image2pixels(self.__image)
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
                self.image2pixels, self.__image, size, self.__resample
            )
            self.__last_image_size = size
        else:
            if isinstance(self.__default, Image):
                self.__content = await asyncio.to_thread(
                    self.image2pixels, self.__default, size, self.__resample
                )
            else:
                self.__content = self.__default
            self.__last_image_size = size
        self.update(self.__content)