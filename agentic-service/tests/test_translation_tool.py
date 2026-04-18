import pytest
from tools.translation_tool import needs_translation, translate_to_english, translate_from_english

def test_needs_translation():
    assert needs_translation("English") == False
    assert needs_translation("en") == False
    assert needs_translation("Hindi") == True
    assert needs_translation("Marathi") == True

def test_translate_to_english():
    assert translate_to_english("Hello", "English") == "Hello"
    assert translate_to_english("गेहूं में पानी कब देना चाहिए", "Hindi") == "When should wheat be irrigated?"
    
def test_translate_from_english():
    assert translate_from_english("Hello", "English") == "Hello"
    assert "Hindi" in translate_from_english("Water them now", "Hindi")
