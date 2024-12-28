import subprocess
import rich_click as click
from rich.tree import Tree
from rich.console import Console
from pathlib import Path
# > Typing
from typing_extensions import List, Union

# ! Metadata

__prog_name__       = 'seaplayer_builder'
__prog_title__      = 'SeaPlayer Builder'
__prog_subtitle__   = None
__prog_version__    = '0.1.0a1'
__prog_author__     = 'Romanin'
__prog_email__      = 'semina054@gmail.com'

# ! Variables

console = Console()

# ! Methods

def searcher_pkgpaths(pkg_dirpath: Union[Path, str]) -> List[str]:
    pkg_dirpath = Path(pkg_dirpath).absolute()
    if not pkg_dirpath.exists():
        raise FileNotFoundError(str(pkg_dirpath))
    if not pkg_dirpath.is_dir():
        raise NotADirectoryError(str(pkg_dirpath))

def generate_args(*args, **kwargs) -> List[str]:
    pass

# ! Main

@click.command()
@click.option(
    '--version', '-V', 'show_version',
    is_flag=True, default=False,
    help='Show the version and exit.'
)
def main(show_version: bool):
    if show_version:
        return main_version(
            __prog_name__,
            __prog_title__,
            __prog_version__,
            __prog_author__
        )

# ! Main > Version

def main_version(name: str, title: str, version: str, author: str):
    output = Tree(f'🌊 [bold green]{title}[/bold green]', highlight=True)
    output.add(f'📌 [#ff8787]{'Version':<8}[/#ff8787]: {version!r}')
    output.add(f'🍑 [#ff8787]{'Author':<8}[/#ff8787]: {author!r}')
    console.print(output)

# ! Run

if __name__ == "__main__":
    main()