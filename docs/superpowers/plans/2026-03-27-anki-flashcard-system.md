# HSK1 Anki Flashcard System — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python pipeline that generates a single `.apkg` Anki package with ~1,400 flashcards for learning Mandarin Chinese (HSK1 + daily/work phrases), with ElevenLabs audio and icon images.

**Architecture:** Three JSON data files feed into three Python scripts: `download_icons.py` fetches icons, `generate_audio.py` calls ElevenLabs, and `build_deck.py` assembles everything into an `.apkg` file using the `genanki` library. All scripts are idempotent — they skip already-generated media.

**Tech Stack:** Python 3.10+, genanki, elevenlabs SDK, requests, python-dotenv

---

## File Map

| File | Purpose |
|------|---------|
| `HSK1/requirements.txt` | Python dependencies |
| `HSK1/.env.example` | Template for API keys |
| `.gitignore` | Ignore .env, media/audio, media/icons, output/, __pycache__ |
| `HSK1/data/vocabulary.json` | ~150 HSK1 words from course PDFs |
| `HSK1/data/daily_phrases.json` | ~70 daily life phrases |
| `HSK1/data/work_phrases.json` | ~80 work/office/tech phrases |
| `HSK1/scripts/config.py` | Paths, API config, voice settings |
| `HSK1/scripts/data_loader.py` | Load & validate all JSON data files |
| `HSK1/scripts/download_icons.py` | Fetch OpenMoji icons → `media/icons/` |
| `HSK1/scripts/generate_audio.py` | ElevenLabs API → `media/audio/` |
| `HSK1/templates/card_styles.css` | Shared Anki card CSS |
| `HSK1/templates/recognition.html` | Type 1 front/back HTML |
| `HSK1/templates/production.html` | Type 2 front/back HTML |
| `HSK1/templates/listening.html` | Type 3 front/back HTML |
| `HSK1/templates/cloze.html` | Type 4 front/back HTML |
| `HSK1/scripts/build_deck.py` | Assemble data + media + templates → .apkg |
| `tests/test_data_loader.py` | Tests for data loading/validation |
| `tests/test_build_deck.py` | Tests for deck building logic |

---

### Task 1: Project Setup & Dependencies

**Files:**
- Create: `HSK1/requirements.txt`
- Create: `HSK1/.env.example`
- Create: `.gitignore`
- Create: `HSK1/scripts/__init__.py`

- [ ] **Step 1: Create requirements.txt**

```
genanki>=0.13.0
elevenlabs>=1.0.0
requests>=2.31.0
pydub>=0.25.1
python-dotenv>=1.0.0
```

Write this to `HSK1/requirements.txt`.

- [ ] **Step 2: Create .env.example**

```
ELEVENLABS_API_KEY=your_key_here
```

Write this to `HSK1/.env.example`.

- [ ] **Step 3: Create .gitignore**

```
# API keys
.env

# Generated media
HSK1/media/audio/
HSK1/media/icons/

# Output
HSK1/output/

# Python
__pycache__/
*.pyc
.venv/

# macOS
.DS_Store
```

Write this to `.gitignore` at the repo root.

- [ ] **Step 4: Create empty __init__.py**

Write an empty file to `HSK1/scripts/__init__.py`.

- [ ] **Step 5: Create virtual environment and install dependencies**

Run:
```bash
cd HSK1 && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

Expected: All packages install successfully.

- [ ] **Step 6: Commit**

```bash
git add .gitignore HSK1/requirements.txt HSK1/.env.example HSK1/scripts/__init__.py
git commit -m "chore: project setup with dependencies and gitignore"
```

---

### Task 2: Config Module

**Files:**
- Create: `HSK1/scripts/config.py`

- [ ] **Step 1: Write config.py**

```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
MEDIA_DIR = BASE_DIR / "media"
AUDIO_DIR = MEDIA_DIR / "audio"
ICONS_DIR = MEDIA_DIR / "icons"
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "output"

# ElevenLabs
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "pNInz6obpgDQGcFmaJgB")  # Default: Adam (male)
ELEVENLABS_MODEL = "eleven_multilingual_v2"
AUDIO_SPEED = 0.85  # Slightly slower for learning

# OpenMoji
OPENMOJI_BASE_URL = "https://openmoji.org/data/color/svg"
ICON_SIZE = 128  # px

# Anki deck
DECK_NAME = "Chinese HSK1"
DECK_ID = 2026032700  # Unique stable ID for the deck
MODEL_ID_BASE = 2026032701  # Base for model IDs (one per card type)

# Data files to load
DATA_FILES = [
    DATA_DIR / "vocabulary.json",
    DATA_DIR / "daily_phrases.json",
    DATA_DIR / "work_phrases.json",
]
```

Write this to `HSK1/scripts/config.py`.

- [ ] **Step 2: Commit**

```bash
git add HSK1/scripts/config.py
git commit -m "feat: add config module with paths and API settings"
```

---

### Task 3: Data Loader with Tests

**Files:**
- Create: `HSK1/scripts/data_loader.py`
- Create: `tests/test_data_loader.py`

- [ ] **Step 1: Write the failing test**

```python
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
```

Write this to `tests/test_data_loader.py`.

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
cd /Users/maximiliano/Repositories/Personal/Chineese && python -m pytest tests/test_data_loader.py -v
```
Expected: ImportError — `data_loader` module doesn't exist yet.

- [ ] **Step 3: Write data_loader.py**

```python
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = [
    "id", "hanzi", "pinyin", "spanish", "english",
    "example_zh", "example_pinyin", "example_es", "example_en",
    "lesson", "tags", "icon"
]


def validate_entry(entry: dict) -> list[str]:
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in entry:
            errors.append(f"Missing required field: {field}")
    return errors


def load_entries(file_paths: list[Path]) -> list[dict]:
    all_entries = []
    seen_ids = set()

    for path in file_paths:
        if not path.exists():
            logger.warning(f"Data file not found, skipping: {path}")
            continue

        with open(path, "r", encoding="utf-8") as f:
            entries = json.load(f)

        for entry in entries:
            errors = validate_entry(entry)
            if errors:
                logger.warning(f"Skipping entry {entry.get('id', '?')}: {errors}")
                continue
            if entry["id"] in seen_ids:
                logger.warning(f"Duplicate ID, skipping: {entry['id']}")
                continue
            seen_ids.add(entry["id"])
            all_entries.append(entry)

    logger.info(f"Loaded {len(all_entries)} entries from {len(file_paths)} files")
    return all_entries
```

Write this to `HSK1/scripts/data_loader.py`.

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
cd /Users/maximiliano/Repositories/Personal/Chineese && python -m pytest tests/test_data_loader.py -v
```
Expected: All 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add HSK1/scripts/data_loader.py tests/test_data_loader.py
git commit -m "feat: add data loader with validation and deduplication"
```

---

### Task 4: HSK1 Vocabulary Data (vocabulary.json)

**Files:**
- Create: `HSK1/data/vocabulary.json`

This is a large data entry task. All ~150 words from the HSK1 vocabulary PDF (Lessons 3–15) must be transcribed into the JSON schema.

- [ ] **Step 1: Create vocabulary.json with all HSK1 words**

Create the file `HSK1/data/vocabulary.json` containing every word from the vocabulary PDF. Each entry must follow the schema defined in Task 3. Words are organized by lesson (3–15). Include all fields: id, hanzi, pinyin, spanish, english, example_zh, example_pinyin, example_es, example_en, lesson, tags, icon.

The `id` format is `hsk1_NNN` with sequential numbering. Tags follow `HSK1::LessonN` format plus a word-category tag (e.g., `nouns`, `verbs`, `particles`, `adjectives`).

Source: The vocabulary PDF pages 1–11 contain all the words. Transcribe every entry.

- [ ] **Step 2: Validate the data**

Run:
```bash
cd /Users/maximiliano/Repositories/Personal/Chineese && python -c "
from HSK1.scripts.data_loader import load_entries
from pathlib import Path
entries = load_entries([Path('HSK1/data/vocabulary.json')])
print(f'Loaded {len(entries)} entries')
assert len(entries) >= 140, f'Expected ~150 entries, got {len(entries)}'
print('All entries valid!')
"
```
Expected: ~150 entries loaded, no validation errors.

- [ ] **Step 3: Commit**

```bash
git add HSK1/data/vocabulary.json
git commit -m "feat: add HSK1 vocabulary data (lessons 3-15)"
```

---

### Task 5: Daily Life Phrases Data (daily_phrases.json)

**Files:**
- Create: `HSK1/data/daily_phrases.json`

- [ ] **Step 1: Create daily_phrases.json with ~70 phrases**

Create the file `HSK1/data/daily_phrases.json`. Each entry follows the same schema. The `id` format is `daily_NNN`. Tags use `daily::greetings`, `daily::food`, `daily::shopping`, `daily::social` prefixes.

**Categories and example content:**

**Greetings & Small Talk (~20):**
- 你好 (Hello), 早上好 (Good morning), 晚上好 (Good evening), 再见 (Goodbye)
- 你最近怎么样？(How have you been?), 周末你做什么了？(What did you do this weekend?)
- 谢谢 (Thank you), 不客气 (You're welcome), 对不起 (Sorry), 没关系 (It's okay)

**Food & Restaurant (~15):**
- 我要这个 (I want this one), 菜单 (menu), 买单 (check please)
- 你推荐什么？(What do you recommend?), 太辣了 (Too spicy)

**Shopping & Transport (~15):**
- 地铁站在哪儿？(Where is the subway station?), 左边/右边 (left/right)
- 太贵了 (Too expensive), 可以便宜一点吗？(Can you make it cheaper?)

**Weather & Social (~20):**
- 今天天气很好 (The weather is nice today), 好冷 (So cold)
- 我们一起吃饭吧 (Let's eat together), 你有空吗？(Are you free?)

All phrases should use HSK1-level grammar. Include complete pinyin, Spanish, and English for every field.

- [ ] **Step 2: Validate the data**

Run:
```bash
cd /Users/maximiliano/Repositories/Personal/Chineese && python -c "
from HSK1.scripts.data_loader import load_entries
from pathlib import Path
entries = load_entries([Path('HSK1/data/daily_phrases.json')])
print(f'Loaded {len(entries)} entries')
assert len(entries) >= 60, f'Expected ~70 entries, got {len(entries)}'
print('All entries valid!')
"
```
Expected: ~70 entries loaded, no validation errors.

- [ ] **Step 3: Commit**

```bash
git add HSK1/data/daily_phrases.json
git commit -m "feat: add daily life phrases data (~70 phrases)"
```

---

### Task 6: Work & Office Phrases Data (work_phrases.json)

**Files:**
- Create: `HSK1/data/work_phrases.json`

- [ ] **Step 1: Create work_phrases.json with ~80 phrases**

Create the file `HSK1/data/work_phrases.json`. Same schema. The `id` format is `work_NNN`. Tags use `work::meetings`, `work::tech`, `work::email`, `work::social`, `work::calls` prefixes.

**Categories and example content:**

**Meeting Language (~20):**
- 我们开始吧 (Let's begin), 你同意吗？(Do you agree?)
- 会议几点开始？(What time does the meeting start?), 下一个话题 (Next topic)
- 我有一个问题 (I have a question), 好的，没问题 (OK, no problem)

**Tech/Engineering (~20):**
- 代码 (code), 测试 (test), 部署 (deploy), 发布 (release)
- 这个有bug (This has a bug), 代码审查 (code review)
- 你能看一下吗？(Can you take a look?), 已经修好了 (Already fixed)

**Email & Chat (~15):**
- 你好！(email opening), 谢谢你的邮件 (Thanks for your email)
- 请确认 (Please confirm), 附件 (attachment), 收到 (Received/Got it)

**Office Social (~15):**
- 一起去吃午饭吧 (Let's go have lunch together)
- 做得好！(Good job!), 辛苦了 (Thanks for your hard work)
- 你能帮我吗？(Can you help me?), 恭喜 (Congratulations)

**Phone/Video Calls (~10):**
- 你能听到吗？(Can you hear me?), 我分享屏幕 (I'll share my screen)
- 你静音了 (You're on mute), 网络不好 (Bad connection)
- 我们用视频吧 (Let's use video)

Include complete pinyin, Spanish, and English for every field. Annotate phrases that exceed HSK1 grammar with a note in the tags (e.g., add `beyond_hsk1` tag).

- [ ] **Step 2: Validate the data**

Run:
```bash
cd /Users/maximiliano/Repositories/Personal/Chineese && python -c "
from HSK1.scripts.data_loader import load_entries
from pathlib import Path
entries = load_entries([Path('HSK1/data/work_phrases.json')])
print(f'Loaded {len(entries)} entries')
assert len(entries) >= 70, f'Expected ~80 entries, got {len(entries)}'
print('All entries valid!')
"
```
Expected: ~80 entries loaded, no validation errors.

- [ ] **Step 3: Commit**

```bash
git add HSK1/data/work_phrases.json
git commit -m "feat: add work and office phrases data (~80 phrases)"
```

---

### Task 7: Card Templates (HTML + CSS)

**Files:**
- Create: `HSK1/templates/card_styles.css`
- Create: `HSK1/templates/recognition.html`
- Create: `HSK1/templates/production.html`
- Create: `HSK1/templates/listening.html`
- Create: `HSK1/templates/cloze.html`

- [ ] **Step 1: Create card_styles.css**

```css
.card {
    font-family: "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
    text-align: center;
    padding: 20px;
    background: #fafafa;
    color: #333;
    max-width: 600px;
    margin: 0 auto;
}

.hanzi {
    font-size: 72px;
    font-weight: bold;
    margin: 20px 0;
    color: #1a1a1a;
}

.pinyin {
    font-size: 28px;
    color: #666;
    margin: 10px 0;
}

/* Tone colors for pinyin */
.tone1 { color: #e74c3c; }  /* red - flat */
.tone2 { color: #2ecc71; }  /* green - rising */
.tone3 { color: #3498db; }  /* blue - dipping */
.tone4 { color: #9b59b6; }  /* purple - falling */
.tone5 { color: #999; }     /* gray - neutral */

.meaning {
    font-size: 22px;
    margin: 10px 0;
}

.meaning-es {
    font-size: 24px;
    color: #2c3e50;
    font-weight: bold;
}

.meaning-en {
    font-size: 18px;
    color: #7f8c8d;
    font-style: italic;
}

.example {
    font-size: 20px;
    margin: 15px 0;
    padding: 12px;
    background: #f0f0f0;
    border-radius: 8px;
    border-left: 4px solid #3498db;
}

.example-zh {
    font-size: 22px;
    color: #1a1a1a;
}

.example-translation {
    font-size: 16px;
    color: #666;
    margin-top: 5px;
}

.icon-img {
    width: 64px;
    height: 64px;
    margin: 10px auto;
    display: block;
}

.cloze-blank {
    display: inline-block;
    min-width: 60px;
    border-bottom: 3px solid #e74c3c;
    margin: 0 5px;
}

.cloze-answer {
    color: #e74c3c;
    font-weight: bold;
}

.listening-prompt {
    font-size: 48px;
    color: #3498db;
    margin: 40px 0;
}

.divider {
    border: none;
    border-top: 1px solid #ddd;
    margin: 15px 0;
}

.label {
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #aaa;
    margin-top: 15px;
}
```

Write this to `HSK1/templates/card_styles.css`.

- [ ] **Step 2: Create recognition.html (Type 1)**

Front template:
```html
<div class="card">
    <img class="icon-img" src="{{icon}}">
    <div class="hanzi">{{hanzi}}</div>
</div>
```

Back template:
```html
<div class="card">
    <img class="icon-img" src="{{icon}}">
    <div class="hanzi">{{hanzi}}</div>
    <div class="pinyin">{{pinyin}}</div>
    <hr class="divider">
    <div class="meaning-es">{{spanish}}</div>
    <div class="meaning-en">{{english}}</div>
    <hr class="divider">
    <div class="example">
        <div class="example-zh">{{example_zh}}</div>
        <div class="example-translation">{{example_pinyin}}</div>
        <div class="example-translation">{{example_es}}</div>
    </div>
    {{audio_word}}
</div>
```

Write both templates (front and back separated by a marker comment `<!-- BACK -->`) to `HSK1/templates/recognition.html`.

- [ ] **Step 3: Create production.html (Type 2)**

Front template:
```html
<div class="card">
    <img class="icon-img" src="{{icon}}">
    <div class="label">ESPAÑOL</div>
    <div class="meaning-es">{{spanish}}</div>
    <div class="label">ENGLISH</div>
    <div class="meaning-en">{{english}}</div>
</div>
```

Back template:
```html
<div class="card">
    <div class="hanzi">{{hanzi}}</div>
    <div class="pinyin">{{pinyin}}</div>
    <hr class="divider">
    <div class="meaning-es">{{spanish}}</div>
    <div class="meaning-en">{{english}}</div>
    {{audio_word}}
</div>
```

Write to `HSK1/templates/production.html`.

- [ ] **Step 4: Create listening.html (Type 3)**

Front template:
```html
<div class="card">
    <div class="listening-prompt">🔊</div>
    <div class="label">LISTEN AND IDENTIFY</div>
    {{audio_word}}
</div>
```

Back template:
```html
<div class="card">
    <div class="hanzi">{{hanzi}}</div>
    <div class="pinyin">{{pinyin}}</div>
    <hr class="divider">
    <div class="meaning-es">{{spanish}}</div>
    <div class="meaning-en">{{english}}</div>
    {{audio_word}}
</div>
```

Write to `HSK1/templates/listening.html`.

- [ ] **Step 5: Create cloze.html (Type 4)**

Front template:
```html
<div class="card">
    <div class="example">
        <div class="example-zh" style="font-size:28px;">{{cloze_sentence}}</div>
    </div>
    <hr class="divider">
    <div class="label">ESPAÑOL</div>
    <div class="example-translation">{{example_es}}</div>
    <div class="label">ENGLISH</div>
    <div class="example-translation">{{example_en}}</div>
</div>
```

Back template:
```html
<div class="card">
    <div class="example">
        <div class="example-zh" style="font-size:28px;">{{example_zh_highlighted}}</div>
        <div class="example-translation">{{example_pinyin}}</div>
    </div>
    <hr class="divider">
    <div class="hanzi" style="font-size:48px;">{{hanzi}}</div>
    <div class="pinyin">{{pinyin}}</div>
    <div class="meaning-es">{{spanish}}</div>
    {{audio_sentence}}
</div>
```

Write to `HSK1/templates/cloze.html`.

- [ ] **Step 6: Commit**

```bash
git add HSK1/templates/
git commit -m "feat: add Anki card HTML templates and CSS styling"
```

---

### Task 8: Icon Download Script

**Files:**
- Create: `HSK1/scripts/download_icons.py`

- [ ] **Step 1: Write download_icons.py**

```python
import logging
import requests
from pathlib import Path

from HSK1.scripts.config import DATA_FILES, ICONS_DIR, OPENMOJI_BASE_URL
from HSK1.scripts.data_loader import load_entries

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Map icon names to OpenMoji hex codes
# Full list at https://openmoji.org/library/
ICON_MAP = {
    # People & Greetings
    "person": "1F9D1",
    "waving-hand": "1F44B",
    "handshake": "1F91D",
    "family": "1F46A",
    "man": "1F468",
    "woman": "1F469",
    "boy": "1F466",
    "girl": "1F467",
    "baby": "1F476",
    "teacher": "1F9D1-200D-1F3EB",
    "student": "1F393",
    "doctor": "1F9D1-200D-2695-FE0F",
    "office-worker": "1F9D1-200D-1F4BC",

    # Objects
    "book": "1F4D6",
    "books": "1F4DA",
    "pen": "1F58A-FE0F",
    "computer": "1F4BB",
    "phone": "1F4F1",
    "television": "1F4FA",
    "chair": "1FA91",
    "table": "1F6CB-FE0F",
    "cup": "2615",
    "car": "1F697",
    "airplane": "2708-FE0F",
    "taxi": "1F695",
    "clothes": "1F45A",
    "money": "1F4B0",
    "name-tag": "1F4DB",

    # Food & Drink
    "rice": "1F35A",
    "food": "1F372",
    "apple": "1F34E",
    "fruit": "1F34F",
    "tea": "1FAD6",
    "water": "1F4A7",
    "restaurant": "1F37D-FE0F",
    "eating": "1F37D-FE0F",
    "cooking": "1F373",
    "delicious": "1F60B",

    # Places
    "house": "1F3E0",
    "school": "1F3EB",
    "hospital": "1F3E5",
    "shop": "1F6D2",
    "china": "1F1E8-1F1F3",
    "usa": "1F1FA-1F1F8",
    "beijing": "1F3EF",
    "building": "1F3E2",
    "subway": "1F687",

    # Actions
    "speaking": "1F5E3-FE0F",
    "writing": "270D-FE0F",
    "reading": "1F4D6",
    "listening": "1F442",
    "looking": "1F440",
    "walking": "1F6B6",
    "sleeping": "1F634",
    "working": "1F4BC",
    "thinking": "1F914",
    "calling": "1F4DE",
    "driving": "1F697",
    "buying": "1F6D2",
    "drinking": "1F964",
    "sitting": "1FA91",

    # Abstract & Grammar
    "grammar": "1F524",
    "question": "2753",
    "number": "1F522",
    "time": "1F552",
    "calendar": "1F4C5",
    "weather": "2600-FE0F",
    "rain": "1F327-FE0F",
    "happy": "1F604",
    "thumbs-up": "1F44D",
    "star": "2B50",
    "check": "2705",
    "speech": "1F4AC",
    "email": "1F4E7",
    "meeting": "1F4CB",
    "screen": "1F5A5-FE0F",
    "microphone": "1F3A4",
    "mute": "1F507",
    "network": "1F310",
    "video": "1F4F9",
    "bug": "1F41B",
    "gear": "2699-FE0F",
    "rocket": "1F680",
    "package": "1F4E6",
    "magnifying-glass": "1F50D",
    "celebration": "1F389",
    "lunch": "1F961",
    "help": "1F198",
    "clock": "1F570-FE0F",
    "arrow-up": "2B06-FE0F",
    "arrow-down": "2B07-FE0F",
    "arrow-left": "2B05-FE0F",
    "arrow-right": "27A1-FE0F",
    "dog": "1F436",
    "cat": "1F431",
    "movie": "1F3AC",
    "body": "1F9CD",
    "some": "1F4CA",
    "big": "1F4CF",
    "small": "1F4CF",
    "many": "1F4CA",
    "few": "1F4CA",
    "year": "1F4C6",
    "return": "21A9-FE0F",
    "come": "1F44B",
    "go": "1F6B6",
    "open": "1F513",
    "close": "1F512",

    # Default fallback
    "default": "1F4A1",
}


def download_icon(icon_name: str, output_dir: Path) -> Path:
    output_path = output_dir / f"{icon_name}.svg"
    if output_path.exists():
        logger.info(f"Icon already exists, skipping: {icon_name}")
        return output_path

    hex_code = ICON_MAP.get(icon_name, ICON_MAP["default"])
    url = f"{OPENMOJI_BASE_URL}/{hex_code}.svg"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        output_path.write_bytes(response.content)
        logger.info(f"Downloaded icon: {icon_name} -> {output_path}")
        return output_path
    except requests.RequestException as e:
        logger.error(f"Failed to download icon {icon_name}: {e}")
        # Try default icon as fallback
        fallback_url = f"{OPENMOJI_BASE_URL}/{ICON_MAP['default']}.svg"
        try:
            response = requests.get(fallback_url, timeout=10)
            response.raise_for_status()
            output_path.write_bytes(response.content)
            logger.warning(f"Used default icon for: {icon_name}")
            return output_path
        except requests.RequestException:
            logger.error(f"Failed to download even default icon for: {icon_name}")
            return output_path


def main():
    ICONS_DIR.mkdir(parents=True, exist_ok=True)
    entries = load_entries(DATA_FILES)

    icon_names = set(entry["icon"] for entry in entries)
    logger.info(f"Downloading {len(icon_names)} unique icons...")

    for icon_name in sorted(icon_names):
        download_icon(icon_name, ICONS_DIR)

    logger.info("Icon download complete!")


if __name__ == "__main__":
    main()
```

Write this to `HSK1/scripts/download_icons.py`.

- [ ] **Step 2: Commit**

```bash
git add HSK1/scripts/download_icons.py
git commit -m "feat: add icon download script with OpenMoji mapping"
```

---

### Task 9: Audio Generation Script

**Files:**
- Create: `HSK1/scripts/generate_audio.py`

- [ ] **Step 1: Write generate_audio.py**

```python
import logging
from pathlib import Path
from elevenlabs import ElevenLabs

from HSK1.scripts.config import (
    AUDIO_DIR, DATA_FILES, ELEVENLABS_API_KEY,
    ELEVENLABS_MODEL, ELEVENLABS_VOICE_ID
)
from HSK1.scripts.data_loader import load_entries

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def generate_audio_file(client: ElevenLabs, text: str, output_path: Path) -> bool:
    if output_path.exists():
        logger.info(f"Audio already exists, skipping: {output_path.name}")
        return True

    try:
        audio_generator = client.text_to_speech.convert(
            voice_id=ELEVENLABS_VOICE_ID,
            model_id=ELEVENLABS_MODEL,
            text=text,
        )
        audio_bytes = b"".join(audio_generator)
        output_path.write_bytes(audio_bytes)
        logger.info(f"Generated audio: {output_path.name}")
        return True
    except Exception as e:
        logger.error(f"Failed to generate audio for '{text}': {e}")
        return False


def main():
    if not ELEVENLABS_API_KEY:
        logger.error("ELEVENLABS_API_KEY not set. Create HSK1/.env with your key.")
        return

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    entries = load_entries(DATA_FILES)

    total = len(entries) * 2  # word + sentence per entry
    generated = 0
    skipped = 0
    failed = 0

    for entry in entries:
        entry_id = entry["id"]

        # Generate word audio
        word_path = AUDIO_DIR / f"{entry_id}_word.mp3"
        if word_path.exists():
            skipped += 1
        elif generate_audio_file(client, entry["hanzi"], word_path):
            generated += 1
        else:
            failed += 1

        # Generate sentence audio
        sentence_path = AUDIO_DIR / f"{entry_id}_sentence.mp3"
        if sentence_path.exists():
            skipped += 1
        elif generate_audio_file(client, entry["example_zh"], sentence_path):
            generated += 1
        else:
            failed += 1

    logger.info(f"Audio generation complete: {generated} generated, {skipped} skipped, {failed} failed (total: {total})")


if __name__ == "__main__":
    main()
```

Write this to `HSK1/scripts/generate_audio.py`.

- [ ] **Step 2: Commit**

```bash
git add HSK1/scripts/generate_audio.py
git commit -m "feat: add ElevenLabs audio generation script"
```

---

### Task 10: Deck Builder Script with Tests

**Files:**
- Create: `HSK1/scripts/build_deck.py`
- Create: `tests/test_build_deck.py`

- [ ] **Step 1: Write the failing test**

```python
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
    assert "____" in result
    assert "叫" not in result
    assert "他" in result


def test_make_cloze_sentence_not_found():
    result = make_cloze_sentence("他叫David", "吃")
    assert "____" not in result
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
```

Write this to `tests/test_build_deck.py`.

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
cd /Users/maximiliano/Repositories/Personal/Chineese && python -m pytest tests/test_build_deck.py -v
```
Expected: ImportError — `build_deck` module doesn't exist yet.

- [ ] **Step 3: Write build_deck.py**

```python
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

        if icon_file.exists():
            if str(icon_file) not in media:
                media.append(str(icon_file))
        else:
            logger.warning(f"Missing icon: {icon_file}")

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
```

Write this to `HSK1/scripts/build_deck.py`.

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
cd /Users/maximiliano/Repositories/Personal/Chineese && python -m pytest tests/test_build_deck.py -v
```
Expected: All 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add HSK1/scripts/build_deck.py tests/test_build_deck.py
git commit -m "feat: add deck builder with 4 card types and media embedding"
```

---

### Task 11: End-to-End Integration Test

**Files:**
- Create: `tests/test_integration.py`

- [ ] **Step 1: Write integration test**

```python
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

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
```

Write this to `tests/test_integration.py`.

- [ ] **Step 2: Run all tests**

Run:
```bash
cd /Users/maximiliano/Repositories/Personal/Chineese && python -m pytest tests/ -v
```
Expected: All tests PASS.

- [ ] **Step 3: Commit**

```bash
git add tests/test_integration.py
git commit -m "test: add end-to-end integration test for full pipeline"
```

---

### Task 12: Update CLAUDE.md and Final Cleanup

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Update CLAUDE.md with build commands**

Update `CLAUDE.md` to include the new project structure, how to set up the environment, and how to run the pipeline:

```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository is a Chinese language learning system that generates Anki flashcard packages (.apkg) from structured JSON data, with AI-generated audio (ElevenLabs) and open-source icons (OpenMoji).

## Structure

- `HSK1/data/` — JSON vocabulary and phrase files (vocabulary, daily life, work)
- `HSK1/scripts/` — Python pipeline scripts (config, data loader, icon downloader, audio generator, deck builder)
- `HSK1/templates/` — Anki card HTML templates and CSS
- `HSK1/media/` — Generated audio and icon files (git-ignored)
- `HSK1/output/` — Generated .apkg files (git-ignored)
- `HSK1/resources/` — Source PDF course materials (Spanish)
- `tests/` — pytest test suite

## Setup

```bash
cd HSK1 && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
cp .env.example .env  # Then add your ElevenLabs API key
```

## Pipeline

Run in order:
```bash
python -m HSK1.scripts.download_icons    # Fetch icons
python -m HSK1.scripts.generate_audio    # Generate audio (requires API key)
python -m HSK1.scripts.build_deck        # Build .apkg
```

## Tests

```bash
python -m pytest tests/ -v
```

## Data Schema

Each entry in the JSON data files follows this structure: id, hanzi, pinyin, spanish, english, example_zh, example_pinyin, example_es, example_en, lesson, tags, icon. See `docs/superpowers/specs/2026-03-27-anki-flashcard-system-design.md` for full spec.
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md with pipeline commands and project structure"
```
