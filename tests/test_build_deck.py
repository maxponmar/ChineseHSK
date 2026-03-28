import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from HSK1.scripts.build_deck import (
    create_models,
    make_cloze_sentence,
    make_highlighted_sentence,
    build_notes_for_entry,
)


def test_make_cloze_sentence():
    result = make_cloze_sentence("他叫David", "叫")
    assert "____" not in result  # Uses HTML span, not literal underscores
    assert "cloze-blank" in result
    assert "叫" not in result.replace("cloze-blank", "")  # hanzi replaced
    assert "他" in result


def test_make_cloze_sentence_not_found():
    result = make_cloze_sentence("他叫David", "吃")
    assert "cloze-blank" not in result
    assert "他叫David" == result


def test_make_highlighted_sentence():
    result = make_highlighted_sentence("他叫David", "叫")
    assert '<span class="cloze-answer">叫</span>' in result


def test_create_models():
    models = create_models()
    assert len(models) == 4
    names = [m.name for m in models]
    assert "HSK1 Recognition" in names
    assert "HSK1 Production" in names
    assert "HSK1 Listening" in names
    assert "HSK1 Cloze" in names


def test_build_notes_for_entry():
    entry = {
        "id": "test_001",
        "hanzi": "你好",
        "pinyin": "nǐ hǎo",
        "spanish": "Hola",
        "english": "Hello",
        "example_zh": "你好！",
        "example_pinyin": "nǐ hǎo!",
        "example_es": "¡Hola!",
        "example_en": "Hello!",
        "lesson": 1,
        "tags": ["daily", "greetings"],
        "icon": "waving-hand"
    }
    models = create_models()
    notes = build_notes_for_entry(entry, models)
    assert len(notes) == 4  # One per card type
