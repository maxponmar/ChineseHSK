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

    total = len(entries) * 2
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
