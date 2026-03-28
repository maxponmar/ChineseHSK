# HSK1 Anki Flashcard System — Design Spec

## Goal

Build a Python pipeline that generates a single Anki `.apkg` file containing ~1,400 flashcards for learning Mandarin Chinese, covering HSK1 vocabulary plus practical daily life and workplace phrases.

## Content Scope

### HSK1 Vocabulary (~150 words)
All vocabulary from the HSK1 course (Lessons 3–15), extracted from `Vocabulario HSK 1.pdf`. Covers: introductions, family, food, time, locations, daily activities, transport, shopping.

### Daily Life Phrases (~70 phrases)
- **Greetings & Small Talk** (~20) — basic greetings, farewells, "how are you", weekend plans
- **Food & Restaurant** (~15) — ordering, recommendations, paying
- **Shopping & Transport** (~15) — directions, buying, taxi/subway
- **Weather & Social** (~20) — weather comments, making plans, expressing feelings

### Work & Office Phrases (~80 phrases)
- **Meeting Language** (~20) — starting/ending meetings, agreeing, scheduling
- **Tech/Engineering** (~20) — code, bug, deploy, release, review, test (Chinese tech terms)
- **Email & Chat** (~15) — opening/closing phrases, requesting info, confirming
- **Office Social** (~15) — lunch invitations, congratulations, asking for help
- **Phone/Video Calls** (~10) — "can you hear me?", screen sharing, "you're on mute"

All extra phrases use HSK1-level grammar where possible, with annotations when stretching beyond it.

## Card Types

Each entry generates 4 cards (~300-350 entries × 4 = ~1,200-1,400 cards total).

### Type 1 — Recognition (汉字 → meaning)
- **Front:** Large hanzi + icon image
- **Back:** Pinyin + Spanish translation + English translation + example sentence + audio (auto-play)

### Type 2 — Production (meaning → 汉字)
- **Front:** Spanish + English meaning + icon image
- **Back:** Hanzi + pinyin + audio

### Type 3 — Listening (audio → meaning)
- **Front:** Audio plays automatically (no text)
- **Back:** Hanzi + pinyin + Spanish + English

### Type 4 — Sentence Cloze (fill the blank)
- **Front:** Example sentence with target word replaced by `____` + Spanish/English sentence translation
- **Back:** Complete sentence with target word highlighted + pinyin + audio of full sentence

## Data Structure

### Source Files

```
HSK1/data/
  vocabulary.json       # ~150 HSK1 words
  daily_phrases.json    # ~70 daily life phrases
  work_phrases.json     # ~80 work/office/tech phrases
```

### Entry Schema

```json
{
  "id": "hsk1_003",
  "hanzi": "叫",
  "pinyin": "jiào",
  "spanish": "Llamarse",
  "english": "To be called",
  "example_zh": "他叫 David",
  "example_pinyin": "tā jiào David",
  "example_es": "Él se llama David",
  "example_en": "He is called David",
  "lesson": 3,
  "tags": ["HSK1", "Lesson3", "verbs"],
  "icon": "name-tag"
}
```

Work/daily phrases use the same schema with different tag prefixes: `work::meetings`, `daily::greetings`, etc.

## Media

### Audio (ElevenLabs)
- **Voice:** Male native Mandarin voice. The script will use ElevenLabs' multilingual v2 model with a male voice. The voice ID is configurable in `config.py` so it can be changed easily.
- **Speed:** Slightly slower than native speed for learning (configurable)
- **Files per entry:**
  - `audio/{id}_word.mp3` — isolated word/phrase
  - `audio/{id}_sentence.mp3` — full example sentence
- **Total:** ~700 audio files

### Icons
- **Source:** OpenMoji (open source) or Flaticon free tier
- **Format:** PNG, 128×128px
- **Strategy:**
  - Concrete nouns → matching icon (狗 → dog)
  - Verbs → action icon (吃 → eating)
  - Abstract words/particles → category icon (grammar puzzle piece)
- **Mapping:** `icon` field in each JSON entry

## Card Styling

Shared CSS in `templates/card_styles.css`. HTML templates per card type in `templates/`. Cards use clean, readable styling with:
- Large hanzi font
- Color-coded pinyin tones
- Icon displayed alongside the word
- Audio player (auto-play on flip for relevant types)

## Project Structure

```
HSK1/
  data/
    vocabulary.json
    daily_phrases.json
    work_phrases.json
  media/
    audio/                   # Generated .mp3 files
    icons/                   # Downloaded .png icons
  templates/
    card_styles.css
    recognition.html
    production.html
    listening.html
    cloze.html
  scripts/
    generate_audio.py        # ElevenLabs API → mp3
    download_icons.py        # Fetch icons → png
    build_deck.py            # Data + media → .apkg
    config.py                # API keys, voice settings, paths
  output/
    HSK1_Complete.apkg       # Final Anki package
  requirements.txt
  .env                       # API keys (git-ignored)
```

## Pipeline

Three scripts, run in order:

1. **`python scripts/download_icons.py`** — Reads all JSON data files, downloads icons for each entry, saves to `media/icons/`
2. **`python scripts/generate_audio.py`** — Reads all JSON data files, generates audio via ElevenLabs API, saves to `media/audio/`
3. **`python scripts/build_deck.py`** — Reads data + media, creates 4 card types per entry, outputs `HSK1_Complete.apkg`

Each script is **idempotent**: skips entries that already have generated media. Re-running after adding new words only processes the new entries.

## Anki Organization

- **Single deck:** "Chinese HSK1"
- **Tags per card:** hierarchical tags for filtering
  - `HSK1::Lesson3`, `HSK1::Lesson4`, ...
  - `daily::greetings`, `daily::food`, `daily::shopping`, `daily::social`
  - `work::meetings`, `work::tech`, `work::email`, `work::social`, `work::calls`
  - `type::recognition`, `type::production`, `type::listening`, `type::cloze`

## Languages

Every card includes both **Spanish** (primary) and **English** (secondary) translations.

## Dependencies

```
genanki          # Anki package generation
elevenlabs       # Text-to-speech API
requests         # HTTP requests for icons
pydub            # Audio format conversion (if needed)
python-dotenv    # .env file loading
```

## Extensibility

The system is designed to scale to HSK2+ by:
- Adding new data files under `HSK2/data/`
- Re-running the same pipeline scripts (they scan data directories)
- Generating separate or combined `.apkg` files

## API Key Configuration

ElevenLabs API key stored in `.env` file (added to `.gitignore`):

```
ELEVENLABS_API_KEY=your_key_here
```
