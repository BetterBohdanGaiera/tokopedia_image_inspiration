"""Configuration module for Tokopedia Fashion Bot."""

import json
import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(Path(__file__).parent.parent / ".env")

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_API = os.getenv("TELEGRAM_BOT_API")

# Tokopedia base URL with Bali location filter
BALI_CITY_IDS = "258,259,260,261,262,263,264,265,476,266"
TOKOPEDIA_BASE_URL = f"https://www.tokopedia.com/search?fcity={BALI_CITY_IDS}&q="

# Gemini model to use (best accuracy for fashion analysis)
GEMINI_MODEL = "gemini-2.5-pro"

# Load reference data
_reference_data_path = Path(__file__).parent.parent / "beach-party-tokopedia-looks.json"


def load_reference_data() -> dict:
    """Load reference data from JSON file."""
    if _reference_data_path.exists():
        with open(_reference_data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


REFERENCE_DATA = load_reference_data()


def validate_config() -> bool:
    """Validate that all required config values are present."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in .env file")
    if not TELEGRAM_BOT_API or TELEGRAM_BOT_API == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        raise ValueError("TELEGRAM_BOT_API is not set in .env file")
    return True
