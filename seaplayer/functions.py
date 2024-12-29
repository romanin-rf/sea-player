import asyncio
import inspect
import itertools
from asyncio import AbstractEventLoop
# > Typing
from typing_extensions import (
    Any,
    Union,
    Iterable, Generator,
    Callable, Coroutine, ParamSpec, Awaitable,
    TypeVar, TypeAlias,
)

# ! Types

T = TypeVar('T')
ReturnType = TypeVar('ReturnType')
Params = ParamSpec('Params')
AsyncMethod: TypeAlias = Callable[..., Coroutine]

# ! Itertools

def iter_dazzle(*iters: Iterable[T]) -> Generator[T, Any, None]:
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


# ! Runner Function

def runner_wrapper(
    loop: AbstractEventLoop,
    func: Union[
        Callable[Params, Coroutine[Any, Any, ReturnType]],
        Awaitable[ReturnType],
        Callable[Params, ReturnType]
    ]
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