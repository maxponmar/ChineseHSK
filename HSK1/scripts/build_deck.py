import logging
from pathlib import Path

import genanki

from HSK1.scripts.config import (
    AUDIO_DIR, DATA_FILES, DECK_ID, DECK_NAME,
    ICONS_DIR, MODEL_ID_BASE, OUTPUT_DIR, TEMPLATES_DIR,
)
from HSK1.scripts.data_loader import load_entries

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def load_template(name: str) -> tuple[str, str]:
    path = TEMPLATES_DIR / f"{name}.html"
    content = path.read_text(encoding="utf-8")
    parts = content.split("<!-- BACK -->")
    front = parts[0].strip()
    back = parts[1].strip() if len(parts) > 1 else ""
    return front, back


def load_css() -> str:
    css_path = TEMPLATES_DIR / "card_styles.css"
    return css_path.read_text(encoding="utf-8")


FIELDS = [
    {"name": "hanzi"},
    {"name": "pinyin"},
    {"name": "spanish"},
    {"name": "english"},
    {"name": "example_zh"},
    {"name": "example_pinyin"},
    {"name": "example_es"},
    {"name": "example_en"},
    {"name": "icon"},
    {"name": "audio_word"},
    {"name": "audio_sentence"},
    {"name": "cloze_sentence"},
    {"name": "example_zh_highlighted"},
]


def create_models() -> list[genanki.Model]:
    css = load_css()
    model_configs = [
        ("HSK1 Recognition", "recognition", MODEL_ID_BASE),
        ("HSK1 Production", "production", MODEL_ID_BASE + 1),
        ("HSK1 Listening", "listening", MODEL_ID_BASE + 2),
        ("HSK1 Cloze", "cloze", MODEL_ID_BASE + 3),
    ]

    models = []
    for name, template_name, model_id in model_configs:
        front, back = load_template(template_name)
        model = genanki.Model(
            model_id=model_id,
            name=name,
            fields=FIELDS,
            templates=[{
                "name": name,
                "qfmt": front,
                "afmt": back,
            }],
            css=css,
        )
        models.append(model)

    return models


def make_cloze_sentence(sentence: str, target: str) -> str:
    if target in sentence:
        return sentence.replace(target, '<span class="cloze-blank">&nbsp;&nbsp;&nbsp;&nbsp;</span>', 1)
    return sentence


def make_highlighted_sentence(sentence: str, target: str) -> str:
    if target in sentence:
        return sentence.replace(target, f'<span class="cloze-answer">{target}</span>', 1)
    return sentence


def build_notes_for_entry(entry: dict, models: list[genanki.Model]) -> list[genanki.Note]:
    entry_id = entry["id"]
    hanzi = entry["hanzi"]

    # Media references
    word_audio_file = f"{entry_id}_word.mp3"
    sentence_audio_file = f"{entry_id}_sentence.mp3"
    icon_file = f"{entry['icon']}.svg"

    audio_word_tag = f"[sound:{word_audio_file}]"
    audio_sentence_tag = f"[sound:{sentence_audio_file}]"
    icon_tag = f'<img class="icon-img" src="{icon_file}">'

    cloze_sentence = make_cloze_sentence(entry["example_zh"], hanzi)
    highlighted_sentence = make_highlighted_sentence(entry["example_zh"], hanzi)

    field_values = [
        entry["hanzi"],
        entry["pinyin"],
        entry["spanish"],
        entry["english"],
        entry["example_zh"],
        entry["example_pinyin"],
        entry["example_es"],
        entry["example_en"],
        icon_tag,
        audio_word_tag,
        audio_sentence_tag,
        cloze_sentence,
        highlighted_sentence,
    ]

    base_tags = list(entry["tags"])
    type_tags = ["type::recognition", "type::production", "type::listening", "type::cloze"]

    notes = []
    for i, model in enumerate(models):
        note = genanki.Note(
            model=model,
            fields=field_values,
            tags=base_tags + [type_tags[i]],
            guid=genanki.guid_for(entry_id, type_tags[i]),
        )
        notes.append(note)

    return notes


def collect_media_files(entries: list[dict]) -> list[str]:
    media = []
    seen_icons = set()
    for entry in entries:
        entry_id = entry["id"]
        icon_name = entry["icon"]

        word_audio = AUDIO_DIR / f"{entry_id}_word.mp3"
        sentence_audio = AUDIO_DIR / f"{entry_id}_sentence.mp3"
        icon_file = ICONS_DIR / f"{icon_name}.svg"

        if word_audio.exists():
            media.append(str(word_audio))
        else:
            logger.warning(f"Missing audio: {word_audio}")

        if sentence_audio.exists():
            media.append(str(sentence_audio))
        else:
            logger.warning(f"Missing audio: {sentence_audio}")

        if icon_name not in seen_icons and icon_file.exists():
            media.append(str(icon_file))
            seen_icons.add(icon_name)
        elif icon_name not in seen_icons:
            logger.warning(f"Missing icon: {icon_file}")
            seen_icons.add(icon_name)

    return media


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    entries = load_entries(DATA_FILES)
    models = create_models()

    deck = genanki.Deck(deck_id=DECK_ID, name=DECK_NAME)

    for entry in entries:
        notes = build_notes_for_entry(entry, models)
        for note in notes:
            deck.add_note(note)

    media_files = collect_media_files(entries)
    output_path = OUTPUT_DIR / "HSK1_Complete.apkg"

    package = genanki.Package(deck)
    package.media_files = media_files
    package.write_to_file(str(output_path))

    logger.info(f"Deck built: {output_path}")
    logger.info(f"Total notes: {len(entries) * 4}")
    logger.info(f"Media files: {len(media_files)}")


if __name__ == "__main__":
    main()
