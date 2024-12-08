from textual.widgets import Input
# > Typing
from typing_extensions import deprecated
from typing import Optional, Tuple, Callable, Awaitable, Any

# ! InputFiles functions
async def conv(value: str) -> Tuple[bool, Optional[Any]]: return True, value
async def submit(input: Input, value: Any) -> None: ...
def update_placeholder() -> Optional[str]: ...

# ! InputField class
@deprecated("It is planned to remove this class.")
class InputField(Input):
    def __init__(
        self,
        conv: Callable[[str], Awaitable[Tuple[bool, Optional[Any]]]]=conv,
        submit: Callable[[Input, Any], Awaitable[None]]=submit,
        update_placeholder: Callable[[], Optional[str]]=update_placeholder,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.__conv = conv
        self.__submit = submit
        self.__update_placeholder = update_placeholder
        if (placeholder:=self.__update_placeholder()) is not None:
            self.placeholder = placeholder
    
    async def action_submit(self):
        value = self.value
        self.value = ""
        if value.replace(" ", "") != "":
            ok, c_value = await self.__conv(value)
            if ok:
                await self.__submit(self, c_value)
        if (placeholder:=self.__update_placeholder()) is not None:
            self.placeholder = placeholder
