import inspect
from textual.widgets import Static
from rich.progress import Progress, BarColumn, TextColumn
# > Typing
from typing_extensions import (
    Any, Tuple,
    Callable, Coroutine, Awaitable
)

# ! Types

GetCallback = \
    Callable[[], Tuple[str, float | None, float | None]] | \
    Callable[[], Coroutine[Any, Any, Tuple[str, float | None, float | None]]] | \
    Callable[[], Awaitable[Tuple[str, float | None, float | None]]]


# ! Main Class

class PlaybackProgress(Static):
    DEFAULT_CSS = """
    PlaybackProgress {
        height: 1;
    }
    """
    
    def __init__(
        self,
        getfunc: GetCallback | None = None,
        refresh_per_second: float = 8.0,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False
    ) -> None:
        self._bar = Progress(BarColumn(), TextColumn('{task.description}'))
        self._task_id = self._bar.add_task('', total=None)
        self._refresh_per_second = refresh_per_second
        if getfunc is not None:
            self._getfunc: GetCallback = getfunc
        else:
            self._getfunc: GetCallback = lambda: ('00:00 / 00:00 |   0%', None, None)
        if inspect.iscoroutinefunction(self._getfunc):
            self.run_mode = 1
        elif inspect.isawaitable(self._getfunc):
            self.run_mode = 2
        elif callable(self._getfunc):
            self.run_mode = 0
        else:
            raise RuntimeError
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
    
    def on_mount(self) -> None:
        self.update_render = self.set_interval(1.0 / self._refresh_per_second, self.update_progress_bar)
    
    async def upgrade_task(
        self,
        description: str = '',
        completed: float | None = None,
        total: float | None = None
    ) -> None:
        self._bar.update(
            self._task_id,
            total=total,
            completed=completed,
            description=description
        )
    
    async def __getting(self) -> Tuple[str, float | None, float | None]:
        if self.run_mode == 0:
            return self._getfunc()
        elif self.run_mode == 1:
            return await self._getfunc()
        elif self.run_mode == 2:
            return await self._getfunc
        return '00:00 |   0%', None, None
    
    async def update_progress_bar(self) -> None:
        d, c, t = await self.__getting()
        needed_width = self.size[0] - len(d) - 1
        if self._bar.columns[0].bar_width != needed_width:
            self._bar.columns[0].bar_width = needed_width
        await self.upgrade_task(completed=c, total=t, description=d)
        self.update(self._bar)