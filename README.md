# Chinese Mandarin Anki Flashcards

A complete Chinese Mandarin learning system that generates Anki flashcard decks (.apkg) with AI-generated audio and visual icons, covering all HSK levels and HSKK oral proficiency.

## Levels

| Level | Words | Description | Status |
|-------|-------|-------------|--------|
| HSK 1 | 150 + 150 extra | Basic vocabulary, daily life & work phrases | Done |
| HSK 2 | ~300 | Elementary conversations | Planned |
| HSK 3 | ~600 | Intermediate daily communication | Planned |
| HSK 4 | ~1200 | Advanced daily & professional topics | Planned |
| HSK 5 | ~2500 | Fluent reading of newspapers & media | Planned |
| HSKK | TBD | Oral proficiency (speaking exam prep) | Planned |

## Features

- **4 card types per word:** Recognition (hanzi -> meaning), Production (meaning -> hanzi), Listening (audio only), Sentence Cloze (fill the blank)
- **Bilingual:** Spanish (primary) + English (secondary) translations
- **AI audio:** Native Mandarin pronunciation via ElevenLabs
- **Visual icons:** OpenMoji icons for visual association
- **Tagged:** Cards tagged by lesson, category, and type for flexible study
- **Work & daily phrases:** Beyond standard HSK vocab — meetings, tech, email, social situations

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r HSK1/requirements.txt
cp HSK1/.env.example HSK1/.env
# Edit HSK1/.env and add your ElevenLabs API key
```

## Generate a Deck

```bash
# Replace HSK1 with the desired level
python -m HSK1.scripts.download_icons
python -m HSK1.scripts.generate_audio
python -m HSK1.scripts.build_deck
```

The output `.apkg` file will be in `HSK1/output/`. Double-click it or import it into Anki.

## Run Tests

```bash
python -m pytest tests/ -v
```

## Project Structure

```
HSK1/                          # One directory per HSK level
  data/
    vocabulary.json            # Core HSK vocabulary
    daily_phrases.json         # Daily life phrases
    work_phrases.json          # Work/office phrases
  scripts/
    config.py                  # Paths, API settings
    data_loader.py             # Load & validate JSON data
    download_icons.py          # Fetch OpenMoji icons
    generate_audio.py          # ElevenLabs TTS
    build_deck.py              # Assemble .apkg package
  templates/
    card_styles.css            # Anki card styling
    recognition.html           # Card type 1
    production.html            # Card type 2
    listening.html             # Card type 3
    cloze.html                 # Card type 4
  resources/                   # Source PDF course materials
  media/                       # Generated audio & icons (git-ignored)
  output/                      # Generated .apkg files (git-ignored)
tests/                         # pytest test suite
```

## Requirements

- Python 3.9+
- [ElevenLabs](https://elevenlabs.io) API key (free tier available)
- [Anki](https://apps.ankiweb.net) desktop app for importing decks

## Attribution

- **Icons:** [OpenMoji](https://openmoji.org) — open-source emoji and icons, licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- **Audio:** Generated using [ElevenLabs](https://elevenlabs.io) text-to-speech API
- **Vocabulary:** Based on the official [HSK](http://www.chinesetest.cn) (Hanyu Shuiping Kaoshi) word lists

## License

This project is licensed under [MIT](LICENSE). Icon assets are subject to their own [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) license.
