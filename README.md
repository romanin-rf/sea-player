<div id="header" align="center">
    <img src="https://github.com/romanin-rf/SeaPlayer/assets/60302782/937adcc4-f547-440c-8139-a5f15bffa157" alt="Icon" width="300">
</div>
<div id="header" align="center"><h1>SeaPlayer</h1></div>

## Descriptions
SeaPlayer is a player that works in the terminal.

Supports the following audio file formats: `MP3`, `OGG`, `WAV`, `FLAC` and more...

Supports the following languages: `English`, `Русский`, `Українська`.

## Screenshots
<!-- ![Main Screen](https://github.com/romanin-rf/SeaPlayer/assets/60302782/84e1f498-beab-463b-ba2a-a8a109e607c0) -->
<!-- ![Configurate Screen](https://github.com/romanin-rf/SeaPlayer/assets/60302782/c8f0fa20-b4b8-4858-ac4a-bb8ddb8c0a39) -->

## Using
```shell
python -m seaplayer # Method for `downloaded repository` or `installed via pip`
```

## Install
1. You can use [Release](https://github.com/romanin-rf/sea-player/releases)
2. ***Download clone repository*** install the dependencies from `requirements.txt` and run via [Python](https://www.python.org).
3.  ```
    pip install -U seaplayer
    ```

<!--
### For MIDI playback
In order to play MIDI files you need to install FluidSynth:
- **Windows**: https://github.com/FluidSynth/fluidsynth/releases
    1. **Download** a zip file suitable for your version of Windows.
    1. **Unpack the archive** anywhere, *but it is recommended to put it in a folder `C:\Program Files\FluidSynth`*
    1. **Next**, open `Settings` > `System` > `About the system` > `Additional system parameters` > `Environment variables` > `[Double click on Path]` > `Create` > `[Enter the full path to the folder with FluidSynth]`
    1. **That's it, FluidSynth is installed!**
- **Linux**:
    - **Ubuntu/Debian**:
        ```shell
        sudo apt-get install fluidsynth
        ```
    - **Arch Linux**:
        ```shell
        sudo pacman -S fluidsynth
        ```
- **MacOS**
    - With [Fink](http://www.finkproject.org/):
        ```shell
        fink install fluidsynth
        ```
    - With [Homebrew](https://brew.sh/):
        ```shell
        brew install fluidsynth
        ```
    - With [MacPorts](http://www.macports.org/):
        ```shell
        sudo port install fluidsynth
        ```
-->