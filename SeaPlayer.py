from rich.console import Console

# ! Variable

console = Console()

# ! Main

def main():
    try:
        from seaplayer.seaplayer import SeaPlayer
        app = SeaPlayer()
        output = app.run()
        if isinstance(output, int):
            exit(output)
    except SystemExit:
        pass
    except:
        console.print_exception(show_locals=True, word_wrap=True)

# ! Start

if __name__ == "__main__":
    main()