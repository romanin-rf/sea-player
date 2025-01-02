import os
import glob
import functools
import properties
# > Typing
from typing_extensions import (
    Dict, List, Tuple,
    Union, Optional,
    _T as T
)
# > Local Imports
from seaplayer.functions import formattrs
from seaplayer.exceptions import LanguageNotExistError, LanguageNotLoadedError

# ! Language Class
class Language:
    """The class reflects the file with the translation."""
    @staticmethod
    def __load_file(filepath: str) -> Dict[str, str]:
        with open(filepath, 'r', errors='ignore', encoding='utf-8') as file:
            return properties.load(file)
    
    def __get_metadata(self) -> Tuple[str, str, str | None, Dict[str, str]]:
        data = self.__load_file(self.__name)
        return \
            data.get("language.metadata.title", f"<LTNF:{self.__mark}>"), \
            data.get("language.metadata.author", "<unknown>"), \
            data.get("language.metadata.author.url", None), \
            {
                "from": data.get("language.metadata.words.from", "from")
            }
    
    # ? Initialization
    def __init__(self, language_filepath: str) -> None:
        """The class reflects the file with the translation.
        
        Args:
            language_filepath (str): The path to the file with the translation.
        
        Raises:
            FileNotFoundError: It is called if the file with the translation does not exist.
        """
        self.__name = os.path.abspath(language_filepath)
        self.__data, self.__loaded = None, False
        # * Checking
        if not os.path.isfile(self.__name):
            raise FileNotFoundError(self.__name)
        # * Metadata Loading
        self.__mark = os.path.splitext(os.path.basename(self.__name))[0].lower()
        self.__title, self.__author, self.__author_url, self.__words = self.__get_metadata()
        # * Clear cache
        self.clear_cache()
    
    # ? Magic Methods
    def __str__(self) -> str:
        attrs = formattrs(
            name=self.__name,
            title=self.__title,
            mark=self.__mark,
            loaded=self.__loaded
        )
        return f"{self.__class__.__name__}({attrs})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    # ? Propertyes
    @property
    def name(self) -> str:
        """The path to the file with the translation.
        
        Returns:
            The full path to the file.
        """
        return self.__name
    
    @property
    def mark(self) -> str:
        """The name of the file without an extension.
        
        Returns:
            The name of the file without the extension.
        """
        return self.__mark
    
    @property
    def title(self) -> str:
        """The name of the translation language taken from the file.
        
        Returns:
            The purpose of the language.
        """
        return self.__title
    
    @property
    def author(self) -> str:
        """The author of the translation taken from the translation file.
        
        Returns:
            The author's nickname.
        """
        return self.__author
    
    @property
    def author_url(self) -> str | None:
        """The link to the author of the translation is taken from the translation file.
        
        Returns:
            Link to the author.
        """
        return self.__author_url
    
    @property
    def words(self) -> Dict[str, str]:
        """Special values that you need to have even if the language is not loaded.
        
        Returns:
            Dictionary of special meanings.
        """
        return self.__words
    
    @property
    def loaded(self) -> bool:
        """If `True`, then the file with the translation is fully loaded in memory.
        
        Returns:
            If loaded, then `True`.
        """
        return self.__loaded
    
    # ? Main Methods
    def load(self) -> None:
        """Full load of the file with the translation in memory."""
        self.__data, self.__loaded = self.__load_file(self.__name), True
    
    def unload(self) -> None:
        """Unload a file with a translation from memory."""
        self.__data, self.__loaded = None, False
    
    @functools.lru_cache(maxsize=1024)
    def get(self, key: str, default: T=None) -> str | T:
        """Getting a line feed.
        
        Args:
            key (str): The key to the variable with the translation, which is registered in the file with the translation.
            default (Optional[str], optional): The default value. Defaults to None.
        
        Raises:
            LanguageNotLoadedError: It is called if the translation file is not fully loaded into memory.
        
        Returns:
            Optional[str]: The translated string.
        """
        if self.loaded:
            return self.__data.get(key, default)
        raise LanguageNotLoadedError()
    
    def clear_cache(self) -> None:
        self.get.cache_clear()

# ! Languages Class
class LanguageLoader:
    """The loader of files with translation."""
    # ? Main Methods
    def __search_langs(self, dlm: str, mlm: str) -> Tuple[Language, Language | None]:
        dl, ml = None, None
        for lang in self.langs:
            if lang.mark == dlm:
                dl = lang
            if lang.mark == mlm:
                ml = lang
        if dl is None:
            raise LanguageNotExistError([dl])
        dl.load()
        if ml is not None:
            ml.load()
        return dl, ml
    
    # ? Initialization
    def __init__(
        self,
        langs_dirpath: str,
        main_lang_mark: str,
        default_lang_mark: str="en-eng",
    ) -> None:
        """The loader of files with translation.
        
        Args:
            langs_dirpath (str): The path to the folder with the translation files.
            main_lang_mark (str): The name of the file with the main translation without the extension.
            default_lang_mark (str, optional): The name of the file with the default translation without an extension. Defaults to "en-eng".
        
        Raises:
            FileNotFoundError: Called if the file with the default translation without the extension could not be found.
        """
        self.__name = os.path.abspath(langs_dirpath)
        self.__mlm = main_lang_mark.lower()
        self.__dlm = default_lang_mark.lower()
        self.__alangs: List[LanguageLoader] = []
        # * Checking
        if not os.path.isdir(self.__name):
            raise FileNotFoundError
        # * Searching and loading languages
        self.__langs: List[Language] = [Language(lp) for lp in glob.glob(os.path.join(self.__name, "??-???.properties"))]
        self.__dlang, self.__mlang = self.__search_langs(self.__dlm, self.__mlm)
        # * Clear cache
        self.clear_cache()
    
    # ? Magic Methods
    def __str__(self) -> str:
        form = formattrs(
            name=self.__name,
            default_lang_mark=self.__dlm,
            main_lang_mark=self.__mlm,
            langs=self.__langs,
            alangs=self.__alangs
        )
        return f"{self.__class__.__name__}({form})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    # ? Propertys
    @property
    def name(self) -> str:
        """The path to the folder with the translation files.
        
        Returns:
            The full path to the file.
        """
        return self.__name
    
    @property
    def main_lang_mark(self) -> str:
        """The name of the file with the main translation without the extension.
        
        Returns:
            The file name without an extension.
        """
        return self.__mlm
    
    @property
    def default_lang_mark(self) -> str:
        """The name of the file with the default translation without an extension.
        
        Returns:
            The file name without an extension.
        """
        return self.__dlm
    
    @property
    def langs(self) -> List[Language]:
        """A list with images of the `Language` class, reflecting the files found in the folder with the translation files.
        
        Returns:
            A list with translations.
        """
        return self.__langs
    
    @property
    def default_lang(self) -> Language:
        """An image of the `Language` class reflecting the uploaded file with the default translation.
        
        Returns:
            The translation.
        """
        return self.__dlang
    
    @property
    def main_lang(self) -> Language | None:
        """An image of the `Language` class reflecting the uploaded file with the main translation.
        
        Returns:
            The translation or `None`.
        """
        return self.__mlang
    
    @property
    def alangs(self):
        """Additional languages, for example, translation of plugins.
        
        Returns:
            A list with an additional translation.
        """
        return self.__alangs
    
    # ? Public Methods
    
    @functools.lru_cache(maxsize=1024)
    def get(self, key: str) -> str:
        """First, it tries to get the translation from the file with the main translation, if it failed, it tries to get it from the file with the default translation, if it failed again, it tries to get them from additional languages (`self.alangs`). If in the end None is still output, then returns the string `"<LTNF>"`, that is, the `Language Text Not Found`.
        
        Args:
            key (str): The key to the variable with the translation, which is registered in the file with the translation.
        
        Returns:
            str: The translated string.
        """
        if self.__mlang is None:
            data = self.__dlang.get(key)
        else:
            data = self.__mlang.get(key, self.__dlang.get(key))
        if data is None:
            for alang in self.__alangs:
                if (data := alang.get(key)) is not None:
                    break
        if data is not None:
            return data
        return f"<LTNF:{key}>"
    
    def merge(self, ll: 'LanguageLoader') -> None:
        """Adding additional languages (`self.alangs`).
        
        Args:
            ll (LanguageLoader): The image of the `LanguageLoader` class.
        """
        assert isinstance(ll, LanguageLoader)
        self.__alangs.append(ll)
    
    def clear_cache(self) -> None:
        self.get.cache_clear()