from textual.widgets import Label
from textual.containers import Center, Vertical, Horizontal
from rich.progress import Progress, BarColumn, TextColumn
# > Typing
from typing import Callable
# > Local Imports
from .Labels import ClickableLabel

# ! RheostatBar Class
class RheostatBar(Label):
    DEFAULT_CSS = """
    RheostatBar {
        height: 1;
    }
    """
    
    def __match_bar_width(self) -> int:
        bar_size = self.size[0] - (len(f"{self.__min_value}{self.__max_value}")+(len(self.__mark)*2)+2)
        if bar_size <= 0:
            bar_size = 4
        return bar_size
    
    def __init__(
        self,
        value: int=0,
        min_value: int=0,
        max_value: int=100,
        mark: str=""
    ) -> None:
        self.__value, self.__min_value, self.__max_value = value, min_value, max_value
        self.__mark = mark
        self.__process = Progress(
            TextColumn(f"{self.__min_value}{self.__mark} "),
            BarColumn(4),
            TextColumn(" {task.total}"+self.__mark)
        )
        self.__tid = self.__process.add_task("", completed=self.__value, total=self.__max_value)
        super().__init__(self.__process, classes="rheostat-bar")
    
    # * Property
    @property
    def value(self) -> int:
        """Currect value."""
        return self.__value
    @value.setter
    def value(self, value: int) -> None:
        self.__process.update(self.__tid, completed=value)
        self.__value = value
        self.update(self.__process)
    
    @property
    def min_value(self) -> int:
        """Minimal value."""
        return self.__min_value
    @min_value.setter
    def min_value(self, value: int) -> None:
        self.__process.columns[0].text_format = f"{value}{self.__mark} "
        self.__min_value = value
        self.update(self.__process)
    
    @property
    def max_value(self) -> int:
        """Maximal value."""
        return self.__max_value
    @max_value.setter
    def max_value(self, value: int) -> None:
        self.__process.columns[2].text_format = " {task.total}"+self.__mark
        self.__max_value = value
        self.update(self.__process)
    
    @property
    def mark(self) -> str:
        """Marking of value.
        Formating:
        ```
        f"{value}{mark}"
        ```
        """
        return self.__mark
    @mark.setter
    def mark(self, value: str) -> None:
        self.__mark = value
        self.max_value = self.max_value
        self.min_value = self.min_value
        self.update(self.__process)
    
    # * Methods
    async def on_resize(self) -> None:
        bar_width = self.__match_bar_width()
        if self.__process.columns[1].bar_width != bar_width:
            self.__process.columns[1].bar_width = bar_width
        self.update(self.__process)

class Rheostat(Vertical):
    DEFAULT_CSS = """
    Rheostat {
        height: 2;
        align-vertical: middle;
    }
    Rheostat Horizontal {
        align-horizontal: center;
        width: 1fr;
    }
    Rheostat Horizontal ClickableLabel {
        width: 1;
        height: 1;
    }
    """
    
    async def __click_plus(self) -> None:
        if (self.bar.value + self.__advance_value) <= self.bar.max_value:
            self.bar.value = self.bar.value + self.__advance_value
            self.label.update(f" {self.bar.value}{self.bar.mark} ")
            self.__on_change_value_method(self.bar.value)
    
    async def __click_minus(self) -> None:
        if (self.bar.value - self.__advance_value) >= self.bar.min_value:
            self.bar.value = self.bar.value - self.__advance_value
            self.label.update(f" {self.bar.value}{self.bar.mark} ")
            self.__on_change_value_method(self.bar.value)
    
    def __init__(
        self,
        on_change_value: Callable[[int], None],
        value: int=0,
        advance_value: int=1,
        min_value: int=0,
        max_value: int=100,
        mark: str=""
    ) -> None:
        self.bar = RheostatBar(value, min_value, max_value, mark)
        self.label = Label(f" {self.bar.value}{self.bar.mark} ")
        self.__advance_value = advance_value
        self.__on_change_value_method = on_change_value
        super().__init__(
            Center(self.bar),
            Horizontal(
                ClickableLabel("-", self.__click_minus),
                self.label,
                ClickableLabel("+", self.__click_plus)
            )
        )