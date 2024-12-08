from rich.console import Console

console = Console()

# ! Start
if __name__ == "__main__":
    try:
        from seaplayer.seaplayer import SeaPlayer
        
        app = SeaPlayer()
        app.run()
        app.started = False
    except:
        console.print_exception(word_wrap=True, show_locals=True)