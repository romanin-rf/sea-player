from typing_extensions import (
    Any,
    Iterable,
    Generator,
)

# ! Error Base Class

class Error(Exception):
    """The base class of the error."""
    def __init__(self, *args, **kwargs) -> None:
        """The base class of the error."""
        super().__init__(*args)
        self.__error_init__(*args, **kwargs)
        self.args = [text for text in self.__error_text__(*args, **kwargs)]
    
    def __error_init__(self, *args, **kwargs) -> None:
        pass
    
    def __error_text__(self, *args, **kwargs) -> Generator[str, Any, None]:
        """Error text generator.
        
        Yields:
            Generator[Optional[str], Any, None]: Returns the error text.
        """
        yield ''

# ! Language Errors

class LanguageNotExistError(Error):
    """The error class indicates that the translation file is missing."""
    
    def __error_init__(self, marks: Iterable[str]=[], *args, **kwargs):
        self.marks = marks
    
    def __error_text__(self, marks: Iterable[str]=[], *args, **kwargs):
        yield f"No language file(s) with such a mark(s) was found: {', '.join([repr(mark) for mark in self.marks])}"

class LanguageNotLoadedError(Error):
    """The error class indicates an unloaded translation file."""
    def __error_text__(self, *args, **kwargs):
        yield f"The language file has not been uploaded. Use the `load` method."

# ! Exceptions

class PathNotExistsError(Exception):
    """An exception class indicating the absence of a path."""
    def __init__(self, path: str) -> None:
        """An exception class indicating the absence of a path."""
        super().__init__()
        self.args = (f"The element along the path {repr(path)} does not exist.",)

class NotBooleanError(Exception):
    """Exception class indicating an error when converting data to `bool`."""
    def __init__(self, data: str) -> None:
        """Exception class indicating an error when converting data to `bool`."""
        super().__init__()
        self.args = (f"The data {repr(data)} cannot be represented as a bool.",)