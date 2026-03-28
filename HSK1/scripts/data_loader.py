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
