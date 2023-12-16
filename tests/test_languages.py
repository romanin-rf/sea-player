import os
import pytest
from seaplayer.languages import LanguageLoader
from seaplayer.units import LANGUAGES_DIRPATH

# ! Vars
ll = LanguageLoader(LANGUAGES_DIRPATH)

# ! Tests
def test_language_count_loaded():
    assert len(ll.alangs) >= len(os.listdir(LANGUAGES_DIRPATH))

def test_language_get_not_exist():
    assert ll.get("") == "<LTNF>"
