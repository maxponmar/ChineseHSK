import json
import tempfile
from pathlib import Path

from HSK1.scripts.data_loader import load_entries, validate_entry


def test_validate_entry_valid():
    entry = {
        "id": "hsk1_001",
        "hanzi": "叫",
        "pinyin": "jiào",
        "spanish": "Llamarse",
        "english": "To be called",
        "example_zh": "他叫 David",
        "example_pinyin": "tā jiào David",
        "example_es": "Él se llama David",
        "example_en": "He is called David",
        "lesson": 3,
        "tags": ["HSK1", "Lesson3"],
        "icon": "name-tag"
    }
    errors = validate_entry(entry)
    assert errors == []


def test_validate_entry_missing_fields():
    entry = {"id": "hsk1_001", "hanzi": "叫"}
    errors = validate_entry(entry)
    assert len(errors) > 0
    assert any("pinyin" in e for e in errors)


def test_load_entries_from_file():
    entries = [
        {
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
    ]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(entries, f, ensure_ascii=False)
        tmp_path = Path(f.name)

    loaded = load_entries([tmp_path])
    assert len(loaded) == 1
    assert loaded[0]["hanzi"] == "你好"
    tmp_path.unlink()


def test_load_entries_skips_missing_files():
    loaded = load_entries([Path("/nonexistent/file.json")])
    assert loaded == []


def test_load_entries_rejects_duplicates():
    entry = {
        "id": "dup_001",
        "hanzi": "好",
        "pinyin": "hǎo",
        "spanish": "Bueno",
        "english": "Good",
        "example_zh": "很好",
        "example_pinyin": "hěn hǎo",
        "example_es": "Muy bueno",
        "example_en": "Very good",
        "lesson": 1,
        "tags": ["HSK1"],
        "icon": "thumbs-up"
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump([entry, entry], f, ensure_ascii=False)
        tmp_path = Path(f.name)

    loaded = load_entries([tmp_path])
    assert len(loaded) == 1
    tmp_path.unlink()
