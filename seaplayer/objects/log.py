import datetime
from enum import IntEnum
from rich.panel import Panel
from rich.traceback import Traceback
from textual.widgets import RichLog
# > Typing
from typing_extensions import (
    Literal
)

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

# ! Colors

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

# ! Textual Log Class

class TextualLogger(RichLog):
    def __init__(self,
        level: TextualLogLevel | None = None,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False
    ) -> None:
        self.log_level = level if (level is not None) else TextualLogLevel.NOTSET
        super().__init__(
            highlight=True, markup=True, wrap=True,
            name=name, id=id, classes=classes, disabled=disabled
        )
    
    def textual_log(
        self,
        level: TextualLogLevel,
        message: str
    ) -> None:
        if level >= self.log_level:
            level_name, level_color = LEVEL_NAMES.get(level, 'UNKNOWN'), LEVEL_COLORS.get(level, '')
            formated_time = '{0.day:0>2}.{0.month:0>2}.{0.year:0>4} {0.hour:0>2}:{0.minute:0>2}:{0.second:0>2}' \
                .format(datetime.datetime.now())
            self.write(f'\\[{formated_time}]\\[[{level_color}]{level_name:^12}[/{level_color}]]: {message}')
    
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
        if TextualLogLevel.ERROR >= self.log_level:
            self.write(Traceback(width=80, word_wrap=True, show_locals=True))
    
    def ln(self, __n: int=1) -> None:
        for _ in range(__n):
            self.write('')
    
    def group(self, title: str, level: TextualLogLevel) -> None:
        if level >= self.log_level:
            self.write(Panel(title, width=80, height=3, highlight=True, style='bold', border_style='magenta'))