import os
import shutil
import platform
from pathlib import Path
from typing import Dict, List

# ! OS Checking
if platform.system() == "Windows":
    ds = ";"
elif platform.system() == "Linux":
    ds = ":"
else:
    raise RuntimeError("Your operating system is not supported.")

# ! Vars
LOCALDIR = os.getcwd()
TRASH_FILES = [ "build", "SeaPlayer.spec" ]
DATA = {
    # * 1) Main Files
    "seaplayer": "seaplayer/",
    "seaplayer/__init__.py": "seaplayer/",
    "seaplayer/__main__.py": "seaplayer/",
    "seaplayer/functions.py": "seaplayer/",
    "seaplayer/seaplayer.py": "seaplayer/",
    "seaplayer/config.py": "seaplayer/",
    "seaplayer/exceptions.py": "seaplayer/",
    "seaplayer/codeсbase.py": "seaplayer/",
    "seaplayer/units.py": "seaplayer/",
    "seaplayer/languages.py": "seaplayer/",
    # * 1.1) Objects
    "seaplayer/objects": "seaplayer/objects/",
    "seaplayer/objects/__init__.py": "seaplayer/objects/",
    "seaplayer/objects/Buttons.py": "seaplayer/objects/",
    "seaplayer/objects/Configurate.py": "seaplayer/objects/",
    "seaplayer/objects/DataOptions.py": "seaplayer/objects/",
    "seaplayer/objects/Labels.py": "seaplayer/objects/",
    "seaplayer/objects/Image.py": "seaplayer/objects/",
    "seaplayer/objects/Input.py": "seaplayer/objects/",
    "seaplayer/objects/Log.py": "seaplayer/objects/",
    "seaplayer/objects/PlayList.py": "seaplayer/objects/",
    "seaplayer/objects/Notification.py": "seaplayer/objects/",
    "seaplayer/objects/ProgressBar.py": "seaplayer/objects/",
    "seaplayer/objects/Radio.py": "seaplayer/objects/",
    "seaplayer/objects/PopUp.py": "seaplayer/objects/",
    # * 1.2) Types
    "seaplayer/types": "seaplayer/types/",
    "seaplayer/types/__init__.py": "seaplayer/types/",
    "seaplayer/types/Convert.py": "seaplayer/types/",
    "seaplayer/types/Cache.py": "seaplayer/types/",
    "seaplayer/types/Environment.py": "seaplayer/types/",
    # * 1.3) Codecs
    "seaplayer/codecs": "seaplayer/codecs/",
    "seaplayer/codecs/__init__.py": "seaplayer/codecs/",
    "seaplayer/codecs/Any.py": "seaplayer/codecs/",
    "seaplayer/codecs/AnySound.py": "seaplayer/codecs/",
    "seaplayer/codecs/MIDI.py": "seaplayer/codecs/",
    "seaplayer/codecs/MP3.py": "seaplayer/codecs/",
    "seaplayer/codecs/OGG.py": "seaplayer/codecs/",
    "seaplayer/codecs/WAV.py": "seaplayer/codecs/",
    "seaplayer/codecs/FLAC.py": "seaplayer/codecs/",
    "seaplayer/codecs/URLS.py": "seaplayer/codecs/",
    # * 1.4) Screens
    "seaplayer/screens": "seaplayer/screens/",
    "seaplayer/screens/__init__.py": "seaplayer/screens/",
    "seaplayer/screens/Configurate.py": "seaplayer/screens/",
    "seaplayer/screens/Unknown.py": "seaplayer/screens/",
    # * 2) Modules Files
    "seaplayer/modules": "seaplayer/modules/",
    "seaplayer/modules/__init__.py": "seaplayer/modules/",
    "seaplayer/modules/colorizer.py": "seaplayer/modules/",
    # * 3) CSS Files
    "seaplayer/css": "seaplayer/css/",
    "seaplayer/css/seaplayer.tcss": "seaplayer/css/",
    "seaplayer/css/configurate.tcss": "seaplayer/css/",
    "seaplayer/css/unknown.tcss": "seaplayer/css/",
    "seaplayer/css/objects.tcss": "seaplayer/css/",
    # * 4) Language Files
    "seaplayer/langs": "seaplayer/langs/",
    "seaplayer/langs/en-eng.properties": "seaplayer/langs/",
    "seaplayer/langs/ru-rus.properties": "seaplayer/langs/",
    "seaplayer/langs/uk-ukr.properties": "seaplayer/langs/",
    # * 5) Assets Files
    "seaplayer/assets": "seaplayer/assets/",
    "seaplayer/assets/image-not-found.png": "seaplayer/assets/"
}

# ! Main Methods
def localize(path: str) -> str:
    return os.path.join(LOCALDIR, path.replace('/', os.sep).replace('\\', os.sep))

def add_datas(data: Dict[str, str]) -> List[str]:
    return [f"--add-data \"{localize(path)}{ds}{data[path]}\"" for path in data]

# ! Runtime Vars
COMMAND_LINE = [
    "pyinstaller", "--noconfirm", "--console", "--clean", "--onefile",
    f"--icon \"{localize('icons/icon.ico')}\"",
    *add_datas(DATA),
    f"\"{localize('SeaPlayer.py')}\""
]
COMMAND = " ".join(COMMAND_LINE)

# ! Starting
print(COMMAND, end="\n\n")
os.system(COMMAND)

# ! Clearing runtime trash
for i in TRASH_FILES:
    path = Path(localize(i))
    try:
        if path.is_dir():
            shutil.rmtree(path.name, ignore_errors=True)
        else:
            os.remove(path.name)
    except:
        pass