from textual.widgets import Label, ListItem, ListView
# > Typing
from typing import Optional, Dict, Sequence
# > Local Import's
from .Labels import FillLabel
from ..codeсbase import CodecBase
from ..functions import get_sound_basename, aiter

# ! Children Classes
class PlayListViewItem(ListItem):
    DEFAULT_CSS = """
    PlayListViewItem {
        height: 4;
    }
    PlayListViewItem .title-label {
        height: 1;
        color: #cacaca;
    }
    PlayListViewItem .subtitle-label {
        height: 1;
        color: #a9a9a9;
    }
    PlayListViewItem FillLabel {
        height: 1;
    }
    """
    
    def __init__(
        self,
        sound: CodecBase,
        sound_sha1: str,
        title: str="",
        first_subtitle: str="",
        second_subtitle: str=""
    ) -> None:
        super().__init__()
        self.title_label = Label(title, classes="title-label")
        self.first_subtitle_label = Label(f" {first_subtitle}", classes="subtitle-label")
        self.second_subtitle_label = Label(f" {second_subtitle}", classes="subtitle-label")
        self.sound = sound
        self.sound_sha1 = sound_sha1
        
        self.compose_add_child(self.title_label)
        self.compose_add_child(self.first_subtitle_label)
        self.compose_add_child(self.second_subtitle_label)
        self.compose_add_child(FillLabel('─'))
    
    async def update_labels(
        self,
        title: Optional[str]=None,
        first_subtitle: Optional[str]=None,
        second_subtitle: Optional[str]=None,
    ) -> None:
        if title is not None: self.title_label.update(title)
        if first_subtitle is not None: self.first_subtitle_label.update(first_subtitle)
        if second_subtitle is not None: self.second_subtitle_label.update(second_subtitle)

# ! Main Class
class PlayListView(ListView):
    DEFAULT_CSS = """
    PlayListView {
        height: 1fr;
    }
    """
    highlighted_child: Optional[PlayListViewItem]
    children: Sequence[PlayListViewItem]
    
    @property
    def currect_sound(self) -> Optional[CodecBase]:
        if self.highlighted_child is not None:
            return self.highlighted_child.sound
    
    @property
    def currect_sound_index(self) -> Optional[int]:
        return self.index
    
    @property
    def currect_sound_sha1(self) -> Optional[str]:
        if self.highlighted_child is not None:
            return self.highlighted_child.sound_sha1
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.sounds: Dict[str, CodecBase] = {}
    
    # ! Sync Methods
    def add_sound(self, sound: CodecBase) -> str:
        sound_sha1 = sound.__sha1__(65536)
        self.sounds[sound_sha1] = sound
        self.append(
            PlayListViewItem(
                sound,
                sound_sha1,
                f"{get_sound_basename(sound)}",
                "{duration} sec, {channel_mode}, {samplerate} Hz, {bitrate} kbps, {codec_name}".format(
                    duration=round(sound.duration),
                    channel_mode="Mono" if sound.channels <= 1 else "Stereo",
                    samplerate=round(sound.samplerate),
                    bitrate=round(sound.bitrate / 1000),
                    codec_name=str(sound.codec_name)
                ),
                sound.__namerepr__()
            )
        )
        return sound_sha1
    
    def exist_sound(self, sound: CodecBase) -> bool:
        check_sound_sha1 = sound.__sha1__(65536)
        child: PlayListViewItem
        for child in self.children:
            if child.sound_sha1 == check_sound_sha1:
                return True
        return False
    
    def get_sound_by_index(self, index: int) -> CodecBase:
        if len(self.children) > index:
            return self.children[index].sound
        raise IndexError(f"There is no `Sound` with such an index: {index}.")
    
    def get_sound_by_sha1(self, sha1: str) -> CodecBase:
        for child in self.children:
            if child.sound_sha1 == sha1:
                return child.sound
        raise IndexError(f"There is no `Sound` with such a sha1: {sha1}")
    
    def get_child_by_index(self, index: int) -> PlayListViewItem:
        if len(self.children) > index:
            return self.children[index]
        raise IndexError(f"There is no `PlayListViewItem` with such an index: {repr(index)}.")
    
    def get_child_by_sha1(self, sha1: str) -> PlayListViewItem:
        for child in self.children:
            if child.sound_sha1 == sha1:
                return child
        raise IndexError(f"There is no `PlayListViewItem` with such a sha1: {repr(sha1)}.")
    
    def get_next_sound_index(self) -> Optional[int]:
        if self.currect_sound_index is not None:
            if len(self.children) > (self.currect_sound_index + 1):
                return self.currect_sound_index + 1
            else:
                return 0
    
    def select_child(self, widget: PlayListViewItem) -> None:
        self._on_list_item__child_clicked(ListItem._ChildClicked(widget))
    
    def select_by_index(self, index: int) -> None:
        self.select_child(self.get_child_by_index(index))
    
    def select_by_sha1(self, sha1: str) -> None:
        self.select_child(self.get_child_by_index(sha1))
    
    def select_next_sound(self) -> None:
        index = self.get_next_sound_index()
        if index is not None:
            self.select_by_index(index)
    
    # ! Async Methods
    async def aio_exist_sound(self, sound: CodecBase) -> bool:
        check_sound_sha1 = await sound.__aio_sha1__(65536)
        child: PlayListViewItem
        async for child in aiter(self.children):
            if child.sound_sha1 == check_sound_sha1:
                return True
        return False
    
    async def aio_add_sound(self, sound: CodecBase) -> str:
        sound_sha1 = await sound.__aio_sha1__(65536)
        self.sounds[sound_sha1] = sound
        await self.append(
            PlayListViewItem(
                sound, sound_sha1,
                f"{get_sound_basename(sound)}",
                "{duration} sec, {channel_mode}, {samplerate} Hz, {bitrate} kbps, {codec_name}".format(
                    duration=round(sound.duration),
                    channel_mode="Mono" if sound.channels <= 1 else "Stereo",
                    samplerate=round(sound.samplerate),
                    bitrate=round(sound.bitrate / 1000),
                    codec_name=str(sound.codec_name)
                ),
                sound.__namerepr__()
            )
        )
        return sound_sha1
    
    async def aio_get_sound_by_index(self, index: int) -> CodecBase:
        if len(self.children) > index:
            return self.children[index].sound
        raise IndexError(f"There is no `Sound` with such an index: {index}.")
    
    async def aio_get_sound_by_sha1(self, sha1: str) -> CodecBase:
        async for child in aiter(self.children):
            if child.sound_sha1 == sha1:
                return child.sound
        raise IndexError(f"There is no `Sound` with such a sha1: {sha1}")
    
    async def aio_get_child_by_index(self, index: int) -> PlayListViewItem:
        if len(self.children) > index:
            return self.children[index]
        raise IndexError(f"There is no `PlayListViewItem` with such an index: {repr(index)}.")
    
    async def aio_get_child_by_sha1(self, sha1: str) -> PlayListViewItem:
        async for child in aiter(self.children):
            if child.sound_sha1 == sha1:
                return child
        raise IndexError(f"There is no `PlayListViewItem` with such a sha1: {repr(sha1)}.")
    
    async def aio_get_next_sound_index(self) -> Optional[int]:
        if self.currect_sound_index is not None:
            if len(self.children) > (self.currect_sound_index + 1):
                return self.currect_sound_index + 1
            else:
                return 0
    
    async def aio_select_child(self, widget: PlayListViewItem) -> None:
        self._on_list_item__child_clicked(ListItem._ChildClicked(widget))
    
    async def aio_select_by_index(self, index: int) -> None:
        await self.aio_select_child(await self.aio_get_child_by_index(index))
    
    async def aio_select_by_sha1(self, sha1: str) -> None:
        await self.aio_select_child(await self.aio_get_child_by_index(sha1))
    
    async def aio_select_next_sound(self) -> None:
        index = await self.aio_get_next_sound_index()
        if index is not None:
            await self.aio_select_by_index(index)