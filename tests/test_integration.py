import json
import tempfile
from pathlib import Path

from HSK1.scripts.data_loader import load_entries
from HSK1.scripts.build_deck import create_models, build_notes_for_entry


def test_full_pipeline_without_media():
    """Test that we can load data and build notes without actual media files."""
    entries = [
        {
            "id": "int_001",
            "hanzi": "你好",
            "pinyin": "nǐ hǎo",
            "spanish": "Hola",
            "english": "Hello",
            "example_zh": "你好！你叫什么？",
            "example_pinyin": "nǐ hǎo! nǐ jiào shénme?",
            "example_es": "¡Hola! ¿Cómo te llamas?",
            "example_en": "Hello! What's your name?",
            "lesson": 1,
            "tags": ["daily::greetings"],
            "icon": "waving-hand"
        },
        {
            "id": "int_002",
            "hanzi": "工作",
            "pinyin": "gōngzuò",
            "spanish": "Trabajar",
            "english": "To work",
            "example_zh": "你在哪儿工作？",
            "example_pinyin": "nǐ zài nǎr gōngzuò?",
            "example_es": "¿Dónde trabajas?",
            "example_en": "Where do you work?",
            "lesson": 9,
            "tags": ["HSK1::Lesson9", "work::social"],
            "icon": "working"
        }
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(entries, f, ensure_ascii=False)
        tmp_path = Path(f.name)

    loaded = load_entries([tmp_path])
    assert len(loaded) == 2

    models = create_models()
    all_notes = []
    for entry in loaded:
        notes = build_notes_for_entry(entry, models)
        assert len(notes) == 4
        all_notes.extend(notes)

    assert len(all_notes) == 8  # 2 entries x 4 card types

    # Verify cloze works
    cloze_note = all_notes[3]  # 4th note of first entry = cloze
    fields = cloze_note.fields
    # cloze_sentence field (index 11) should have blank
    assert "cloze-blank" in fields[11]
    # highlighted field (index 12) should have answer
    assert "cloze-answer" in fields[12]

    tmp_path.unlink()
