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
