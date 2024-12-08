from rich.progress import Progress, BarColumn, TextColumn
from textual.widgets import Static, Label
# > Typing
from typing import Optional, Callable, Coroutine, Tuple, Any
# > Local Import's
from ..functions import get_bar_status

# ! Main Class
class IndeterminateProgress(Static):
    DEFAULT_CSS = """
    IndeterminateProgress {
        height: 1;
    }
    """
    
    def __init__(
        self,
        getfunc: Callable[[], Coroutine[Any, Any, Tuple[str, Optional[float], Optional[float]]]]=get_bar_status,
        fps: int=10
    ) -> None:
        super().__init__()
        self._bar = Progress(BarColumn(), TextColumn("{task.description}"))
        self._task_id = self._bar.add_task("", total=None)
        self._fps = fps
        self._getfunc = getfunc
    
    def on_mount(self) -> None:
        self.update_render = self.set_interval(1/self._fps, self.update_progress_bar)
    
    async def upgrade_task(self, description: str="", completed: Optional[float]=None, total: Optional[float]=None) -> None:
        self._bar.update(self._task_id, total=total, completed=completed, description=description)
    
    async def update_progress_bar(self) -> None:
        d, c, t = await self._getfunc()
        if self._bar.columns[0].bar_width != (self.size[0]-len(d)-1):
            self._bar.columns[0].bar_width = self.size[0]-len(d)-1
        await self.upgrade_task(completed=c, total=t, description=d)
        self.update(self._bar)


