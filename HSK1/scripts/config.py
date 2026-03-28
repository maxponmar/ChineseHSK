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
