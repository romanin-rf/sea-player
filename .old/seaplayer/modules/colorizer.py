from typing import Dict
from typing_inspect import (
    is_optional_type,
    is_union_type,
    is_literal_type,
    is_tuple_type,
    get_args,
    get_origin
)

# ! Vars
REPLACE_TYPES = {
    "str": "[green]str[/green]",
    "bool": "[green]bool[/green]",
    "int": "[green]int[/green]",
    "float": "[green]float[/green]",
    "bytes": "[green]bytes[/green]",
    "bytearray": "[green]bytearray[/green]",
    "complex": "[green]complex[/green]",
    "list": "[green]list[/green]",
    "tuple": "[green]tuple[/green]",
    "dict": "[green]dict[/green]",
    "None": "[cyan]None[/cyan]",
    "Tuple": "[green]Tuple[/green]",
    "Dict": "[green]Dict[/green]",
    "List": "[green]List[/green]",
    "Any": "[white]Any[/white]",
    "Literal": "[green]Literal[/green]",
    "['": "[[yellow]'",
    ", '": ", [yellow]'",
    "']": "'[/yellow]]",
    "', ": "'[/yellow], "
}

# ! Other Functions
def is_list_type(tp) -> bool: return get_origin(tp) == list
def is_dict_type(tp) -> bool: return get_origin(tp) == dict
def replaces(string: str, replacement: Dict[str, str]) -> str:
    for _old, _new in replacement.items(): string = string.replace(_old, _new)
    return string

# ! Functions
def pullyper(tp: type) -> str:
    if tp is None:
        return "None"
    elif is_optional_type(tp):
        return f"{pullyper(get_args(tp)[0])} | None"
    elif is_union_type(tp):
        return " | ".join(pullyper(arg) for arg in get_args(tp))
    elif is_literal_type(tp):
        return f"Literal[{', '.join(repr(arg) for arg in get_args(tp))}]"
    elif is_tuple_type(tp):
        if len(args:=get_args(tp)) > 0:
            return f"Tuple[{', '.join(pullyper(arg) for arg in args)}]"
        return "Tuple"
    elif is_list_type(tp):
        if len(args:=get_args(tp)) > 0:
            return f"List[{pullyper(args[0])}]"
        return "List"
    elif is_dict_type(tp):
        if len(args:=get_args(tp)) > 0:
            return f"Dict[{', '.join(pullyper(arg) for arg in args)}]"
        return "Dict"
    else:
        return tp.__name__

def richefication(tp: type) -> str:
    return replaces(pullyper(tp), REPLACE_TYPES)