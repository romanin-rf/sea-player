import sys
import subprocess

# ! Main Class
class PIPManager:
    def __init__(self) -> None:
        self.python_path = sys.executable
    
    def __call__(self, *args: str) -> str:
        return subprocess.check_output([self.python_path, "-m", "pip", *args]).decode(errors="ignore")
    
    def install(self, *args: str) -> str:
        return self.__call__("install", *args)
    
    def install_requirements(self, filepath: str, upgrade: bool=False) -> str:
        cmd = ["-U", "-r", filepath] if upgrade else ["-r", filepath]
        return self.install(*cmd)

# ! Initial
pip = PIPManager()