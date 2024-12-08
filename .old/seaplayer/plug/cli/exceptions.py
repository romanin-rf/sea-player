class PluginNotExistsError(Exception):
    def __init__(self, name_id: str) -> None:
        super().__init__()
        self.args = (f"The {repr(name_id)} plugin was not found.",)

class IsPluginDirectoryError(Exception):
    def __init__(self, dirpath: str) -> None:
        super().__init__()
        self.args = (f"There is already a plugin in this directory: {repr(dirpath)}.",)

class IsNotPluginDirectoryError(Exception):
    def __init__(self, dirpath: str) -> None:
        super().__init__()
        self.args = (f"Not the plugin directory: {repr(dirpath)}.",)