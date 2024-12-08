from vbml import Pattern, Patcher
# > Typing
from typing import Optional, Dict, Any

# ! VBML Objects
PATCHER = Patcher()

VKM_SUID_PATTERN =                  Pattern("vkm://by/users?uid=<uid:int>&sid=<sid:int>")           # !
VKM_RANGE_SUID_PATTERN =            Pattern("vkm://by/users?uid=<uid:int>?r=<ssid:int>-<esid:int>") # >
VKM_TEXT_PATTERN =                  Pattern("vkm://by/text?t=<text>")                               # >
VKM_TEXT_RANGE_PATTERN =            Pattern("vkm://by/text?t=<text>&c=<count:int>")                 # >
VKM_TEXT_RANGE_OFFSET_PATTERN =     Pattern("vkm://by/text?t=<text>&c=<count:int>&o=<offset:int>")  # !

VKM_SUID_FORMAT =                   "vkm://by/users?uid={uid}&sid={sid}"
VKM_TEXT_RANGE_OFFSET_FORMAT =      "vkm://by/text?t={text}&c={count}&o={offset}"

# ! For VBML methods
def pget(pattern: Pattern, text: str) -> Optional[Dict[str, Any]]:
    if isinstance(data:=PATCHER.check(pattern, text), dict):
        return data

def pcheck(pattern: Pattern, text: str) -> bool:
    return isinstance(PATCHER.check(pattern, text), dict)

def pchecks(text: str, *patterns: Pattern) -> bool:
    return max([pcheck(pattern, text) for pattern in patterns])