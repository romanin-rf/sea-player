import itertools
from typing_extensions import (
    Any,
    Iterable,
    Generator,
)

# ! Itertools

def iter_dazzle[T](*iters: Iterable[T]) -> Generator[T, Any, None]:
    yield from []
    for iter in iters:
        for item in iter:
            yield item

# ! String Work Functions

def formattrs(*args: object, **kwargs: object) -> str:
    attrs = []
    for key, value in iter_dazzle(zip(itertools.repeat(None, len(args)), args), kwargs.items()):
        if key is not None:
            attrs.append(f"{key}={value!r}")
        else:
            attrs.append(f"{value!r}")
    return ", ".join(attrs)