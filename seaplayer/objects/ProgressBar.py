from textual.widgets import Static, ProgressBar
from rich.progress import Progress, BarColumn, TextColumn
# > Typing
from typing_extensions import Optional, Callable, Tuple

# ! Main Class

class PlaybackProgress(Static):
    DEFAULT_CSS = """
    IndeterminateProgress {
        height: 1;
    }
    """
    
    def __init__(
        self,
        getfunc: Optional[Callable[[], Tuple[str, Optional[float], Optional[float]]]]=None,
        fps: int=8
    ) -> None:
        super().__init__()
        self._bar = Progress(BarColumn(), TextColumn("{task.description}"))
        self._task_id = self._bar.add_task("", total=None)
        self._fps = fps
        if getfunc is not None:
            self._getfunc = getfunc
        else:
            self._getfunc = lambda: ("00:00 |   0%", None, None)
    
    def on_mount(self) -> None:
        self.update_render = self.set_interval(1 / self._fps, self.update_progress_bar)
    
    async def upgrade_task(
        self,
        description: str="",
        completed: Optional[float]=None,
        total: Optional[float]=None
    ) -> None:
        self._bar.update(
            self._task_id,
            total=total,
            completed=completed,
            description=description
        )
    
    async def update_progress_bar(self) -> None:
        d, c, t = self._getfunc()
        needed_width = self.size[0] - len(d) - 1
        if self._bar.columns[0].bar_width != needed_width:
            self._bar.columns[0].bar_width = needed_width
        await self.upgrade_task(completed=c, total=t, description=d)
        self.update(self._bar)