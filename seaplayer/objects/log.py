import datetime
from enum import IntEnum
from rich.panel import Panel
from rich.text import Text
from rich.traceback import Traceback
from textual.widgets import RichLog
# > Typing
from typing_extensions import IO

# ! Types

class TextualLogLevel(IntEnum):
    NOTSET = 0
    TRACE = 10
    INFO = 20
    DEBUG = 30
    WARNING = 40
    ERROR = 50
    CRITICAL = 100
    OFF = 1000

# ! Constants

LEVEL_COLORS = {
    TextualLogLevel.NOTSET: '#808080',
    TextualLogLevel.TRACE: '#808080',
    TextualLogLevel.DEBUG: 'magenta',
    TextualLogLevel.INFO: 'green',
    TextualLogLevel.WARNING: 'orange',
    TextualLogLevel.ERROR: 'red',
    TextualLogLevel.CRITICAL: 'bold red on white',
}

LEVEL_NAMES = {
    TextualLogLevel.NOTSET: 'NOTSET',
    TextualLogLevel.TRACE: 'TRACE',
    TextualLogLevel.DEBUG: 'DEBUG',
    TextualLogLevel.INFO: 'INFO',
    TextualLogLevel.WARNING: 'WARNING',
    TextualLogLevel.ERROR: 'ERROR',
    TextualLogLevel.CRITICAL: 'CRITICAL',
}

DEFAULT_FORMAT_TIME = '{0.day:0>2}.{0.month:0>2}.{0.year:0>4} {0.hour:0>2}:{0.minute:0>2}:{0.second:0>2}'
DEFAULT_FORMAT_LEVEL = '[{color}]{name:^11}[/{color}]'
DEFAULT_FORMAT_LOG = '\\[{time}]\\[{level}]: {message}'

# ! Textual Log Class

class TextualLogger(RichLog):
    def __init__(self,
        level: TextualLogLevel | None = None,
        io: IO[str] | None = None,
        format_time: str = DEFAULT_FORMAT_TIME,
        format_level: str = DEFAULT_FORMAT_LEVEL,
        format_log: str = DEFAULT_FORMAT_LOG,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False
    ) -> None:
        self.level = level if (level is not None) else TextualLogLevel.NOTSET
        self.io = io
        self.format_time = format_time
        self.format_level = format_level
        self.format_log = format_log
        super().__init__(
            highlight=True, markup=True, wrap=True,
            name=name, id=id, classes=classes, disabled=disabled
        )
    
    def _iowrite(self, line: str) -> int:
        if self.io is not None:
            if not self.io.closed:
                return self.io.write(Text.from_markup(line).plain + '\n')
        return 0
    
    def textual_log(
        self,
        level: TextualLogLevel,
        message: str
    ) -> None:
        if level >= self.level:
            level_name, level_color = LEVEL_NAMES.get(level, 'UNKNOWN'), LEVEL_COLORS.get(level, '')
            ftime, flevel = \
                self.format_time.format(datetime.datetime.now()), \
                self.format_level.format(name=level_name, color=level_color)
            line = self.format_log.format(time=ftime, level=flevel, message=message)
            self.write(line)
            self._iowrite(line)
    
    def trace(self, message: str) -> None:
        self.textual_log(TextualLogLevel.TRACE, message)
    
    def debug(self, message: str) -> None:
        self.textual_log(TextualLogLevel.DEBUG, message)
    
    def info(self, message: str) -> None:
        self.textual_log(TextualLogLevel.INFO, message)
    
    def warning(self, message: str) -> None:
        self.textual_log(TextualLogLevel.WARNING, message)
    
    def error(self, message: str) -> None:
        self.textual_log(TextualLogLevel.ERROR, message)
    
    def critical(self, message: str) -> None:
        self.textual_log(TextualLogLevel.CRITICAL, message)
    
    def exception(self) -> None:
        if TextualLogLevel.ERROR >= self.level:
            self.write(Traceback(width=80, word_wrap=True, show_locals=True))
    
    def ln(self, __n: int=1) -> None:
        for _ in range(__n):
            self.write('')
    
    def group(self, title: str, level: TextualLogLevel) -> None:
        if level >= self.level:
            self.write(Panel(title, width=80, height=3, highlight=True, style='bold', border_style='magenta'))