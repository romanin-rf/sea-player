from typing_extensions import Set

# ! Locker Main Class

class Locker:
    def __init__(self, *args, **kwargs) -> None:
        self.locks: Set[str] = set()
    
    def acquire(self, name: str, /) -> None:
        self.locks.add(name)
    
    def release(self, name: str) -> None:
        try:
            self.locks.remove(name)
        except KeyError:
            return
    
    def locked(self, name: str, /) -> bool:
        return name in self.locks