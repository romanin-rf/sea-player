import time
# > Typing
from typing_extensions import List, Tuple

# ! Timer Class

class Timer:
    def __init__(self) -> None:
        self.__start_time: float = 0.0
        self.__end_time: float = 0.0
    
    def __enter__(self):
        self.__start_time = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.__end_time = time.perf_counter()
    
    def __str__(self) -> str:
        return f"{self.duration:.3f}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__str__()})"
    
    def __float__(self) -> float:
        return self.duration
    
    def __int__(self) -> int:
        return round(self.duration)
    
    @property
    def start_time(self) -> float:
        return self.__start_time
    
    @property
    def end_time(self) -> float:
        return self.__end_time
    
    @property
    def duration(self) -> float:
        return self.__end_time - self.__start_time
    
    def start(self) -> None:
        self.__start_time = time.perf_counter()
    
    def end(self) -> None:
        self.__end_time = time.perf_counter()

# ! Segment Timer Class

class SegmentTimer:
    def __init__(self) -> None:
        self.__segments: List[Tuple[float, float]] = []
        self.__index: int | None = None
    
    @property
    def duration(self) -> float:
        dur = 0.0
        for start_time, end_time in self.__segments:
            dur += end_time - start_time
        return dur
    
    def __str__(self) -> str:
        return f"{self.duration:.3f}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__str__()})"
    
    def __float__(self) -> float:
        return self.duration
    
    def __int__(self) -> int:
        return round(self.duration)
    
    def __format__(self, format_spec: str) -> str:
        return self.duration.__format__(format_spec)
    
    def __enter__(self):
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release()
    
    def acquire(self) -> None:
        if self.__index is None:
            self.__index = len(self.__segments)
            self.__segments.append( (time.perf_counter(), 0.0) )
    
    def release(self) -> None:
        if self.__index is not None:
            end_time = time.perf_counter()
            self.__segments[self.__index] = (self.__segments[self.__index][0], end_time)
            self.__index = None