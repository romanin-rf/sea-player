import asyncio
import rich_click as click
from rich.console import Console
# > Typing
from typing_extensions import Literal

# ! Variable

console = Console()

# ! SeaPlayer Main

def seaplayer_main(
    run_method: Literal['async', 'sync'],
    **kwargs
) -> None:
    try:
        from seaplayer.seaplayer import SeaPlayer
        app = SeaPlayer()
        if run_method == 'async':
            output = asyncio.run(app.run_async(**kwargs))
        elif run_method == 'sync':
            output = app.run(**kwargs)
        else:
            raise ValueError(f'{run_method=}')
        if isinstance(output, int):
            exit(output)
    except SystemExit as e:
        exit(e.code)
    except KeyboardInterrupt:
        exit(0)
    except:
        console.print_exception(show_locals=True, word_wrap=True, width=console.width, max_frames=0)
        exit(1)

# ! SeaPlayer CLI

@click.command()
@click.option(
    '--run-method', 'run_method',
    type=click.Choice(['sync', 'async']), default='async', show_default=True,
    help='Choosing the launch method in which the application will run.'
)
@click.option(
    '--no-headless/--headless', 'headless',
    is_flag=True, type=click.BOOL, default=False,
    help='Run in headless mode (no output).'
)
@click.option(
    '--no-inline/--inline', 'inline',
    is_flag=True, type=click.BOOL, default=False,
    help='Run the app inline (under the prompt).'
)
@click.option(
    '--inline-clear/--inline-no-clear', 'inline_no_clear',
    is_flag=True, type=click.BOOL, default=False,
    help='Run the app inline (under the prompt).'
)
@click.option(
    '--mouse/--no-mouse', 'mouse',
    is_flag=True, type=click.BOOL, default=True,
    help='Enable mouse support.'
)
def main(
    run_method: Literal['async', 'sync'],
    headless: bool,
    inline: bool,
    inline_no_clear: bool,
    mouse: bool,
) -> None:
    seaplayer_main(
        run_method=run_method,
        headless=headless,
        inline=inline,
        inline_no_clear=inline_no_clear,
        mouse=mouse,
    )
