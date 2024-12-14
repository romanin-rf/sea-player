import os
import pickle
# > Typing
from typing_extensions import (
    Any,
    TypeVar
)

# ! Type Vars
D = TypeVar("D")

# ! Main Class
class Cacher:
    """The caching management class."""
    def __init__(self, cache_dirpath: str) -> None:
        """The caching management class.
        
        Args:
            cache_dirpath (str): The path to the directory with the cache.
        """
        self.main_dirpath = os.path.abspath(cache_dirpath)
        self.vars_dirpath = os.path.join(self.main_dirpath, "vars")
        # * Create Directory
        os.makedirs(self.main_dirpath, 0o755, True)
        os.makedirs(self.vars_dirpath, 0o755, True)
        # * Check Directory
        assert os.path.isdir(self.main_dirpath)
        assert os.path.isdir(self.vars_dirpath)
    
    # ! I/O Methods
    def write(self, data: Any, filepath: str) -> None:
        with open(filepath, "wb") as file:
            pickle.dump(data, file)
    
    def read(self, filepath: str, default: D) -> D:
        try:
            with open(filepath, "rb") as file:
                return pickle.load(file, encoding='utf-8')
        except:
            self.write(default, filepath)
            return default
    
    # ! Var Methods
    def write_var(self, value: Any, name: str, *, group: str="main") -> None:
        self.write(value, os.path.join(self.vars_dirpath, f"{name}-{group}.pycache"))
    
    def read_var(self, name: str, default: D, *, group: str="main") -> D:
        return self.read(os.path.join(self.vars_dirpath, f"{name}-{group}.pycache"), default)
    
    # ! Main Methods
    def var(self, name: str, default: D, *, group: str="main") -> D:
        """Caching a variable, wraps the value of the variable in `property` and saves it when the value is changed, and the next time SeaPlayer is started, the value is loaded from the cache.
        
        Args:
            name (str): The name of the cached variable.
            default (D): The default value of the variable.
            group (str, optional): A group of variables. Defaults to "main".
        
        Returns:
            D: Returns `property`, but as part of convenience, typing has been done that says that the same type that was set is returned.
        """
        def setter(s, value: D) -> None:
            self.write_var(value, name, group=group)
        def getter(s) -> D:
            return self.read_var(name, default, group=group)
        return property(getter, setter)
