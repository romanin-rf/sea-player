import asyncio
import inspect
import itertools
# > Typing
from typing_extensions import (
    Any,
    Iterable, Generator,
    Callable, Coroutine, ParamSpec, Awaitable,
    Type, TypeVar, TypeAlias,
)

# ! Types

T                           = TypeVar('T')
ReturnType                  = TypeVar('ReturnType')
Params                      = ParamSpec('Params')
AsyncMethod: TypeAlias      = Callable[..., Coroutine]

# ! Itertools

def iter_dazzle(*iters: Iterable[T]) -> Generator[T, Any, None]:
    yield from []
    for iter in iters:
        for item in iter:
            yield item

def exist_by_type(__type: Type[T], __iter: Iterable[T | object]) -> bool:
    for item in __iter:
        if isinstance(item, __type):
            return True
    return False

# ! String Work Functions

def formattrs(*args: object, **kwargs: object) -> str:
    attrs = []
    for key, value in iter_dazzle(zip(itertools.repeat(None, len(args)), args), kwargs.items()):
        if key is not None:
            attrs.append(f"{key}={value!r}")
        else:
            attrs.append(f"{value!r}")
    return ", ".join(attrs)


# ! Runner Function

def runner_wrapper(
    func:
        Callable[Params, Coroutine[Any, Any, ReturnType]] |
        Awaitable[ReturnType] |
        Callable[Params, ReturnType]
) -> Callable[Params, ReturnType]:
    if inspect.iscoroutinefunction(func):
        def runner_wrapped(*args: Params.args, **kwargs: Params.kwargs) -> ReturnType:
            return asyncio.run(func(*args, **kwargs))
    elif inspect.isawaitable(func):
        async def await_wrapper(*args: Params.args, **kwargs: Params.kwargs):
            return await func
        def runner_wrapped(*args: Params.args, **kwargs: Params.kwargs):
            return asyncio.run(await_wrapper(*args, **kwargs))
    elif callable(func):
        runner_wrapped = func
    else:
        raise TypeError(func)
    return runner_wrapped