from .seaplayer import SeaPlayer
from rich.console import Console

console = Console()

# ! Run Functions
def run() -> None:
    try:
        app = SeaPlayer()
        app.run()
        app.started = False
    except:
        console.print_exception(word_wrap=True, show_locals=True)

# ! Start
if __name__ == "__main__":
    run()