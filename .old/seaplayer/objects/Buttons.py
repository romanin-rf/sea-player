import asyncio
from rich.text import TextType
from textual.widgets import Button
# > Typing
from typing import Optional, Callable, Awaitable

# ! Clikable Button Class
class ClikableButton(Button):
    """The widget responds to clicks."""
    def __init__(
        self,
        label: str,
        on_click: Callable[[], Awaitable[None]],
        *args,
        **kwargs
    ) -> None:
        """A widget that calls the `on_click` function after clicking on it.
        
        Args:
            label (str): The text inside the widget.
            on_click (Callable[[], Awaitable[None]]): The function that is called after clicking on the widget.
        """
        super().__init__(label, *args, **kwargs)
        self.__on_click_method = on_click
    
    async def on_click(self, *args, **kwargs) -> None:
        await self.__on_click_method()

# ! Wait Button Click
class WaitButton(Button):
    """A widget with the function of waiting for a click."""
    def __init__(
        self,
        label: Optional[TextType]=None,
        queue_max_size: int=1,
        *args,
        **kwargs
    ) -> None:
        """_summary_
        
        Args:
            label (Optional[TextType], optional): _description_. Defaults to None.
            queue_max_size (int, optional): _description_. Defaults to 1.
        """
        super().__init__(label, *args, **kwargs)
        self.__wait_queue: asyncio.Queue[bool] = asyncio.Queue(queue_max_size)
    
    async def on_click(self, *args, **kwargs) -> None:
        await self.__wait_queue.put(True)
    
    async def wait_click(self) -> bool:
        """A function that includes waiting for a click.
        
        Returns:
            bool: Always returns `True`.
        """
        return await self.__wait_queue.get()