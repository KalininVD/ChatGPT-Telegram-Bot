# Import necessary modules
from os import path
import json
import logging  # Import logging module

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Get the absolute path to the translations.json file
filepath = path.abspath(path.join(path.dirname(__file__), "..", "translations.json"))

# Load translations from the JSON file
translations = json.load(open(filepath))

# Retrieve message based on user language
def get_translation(language_code: str, key: str) -> str:
    if language_code not in [translation['code'] for translation in translations]:
        logger.warning(f"Language code '{language_code}' is not recognized.")
        return translations[0]['content'].get(key, f"Translation missing for key: {key}")

    for translation in translations:
        if translation['code'] == language_code:
            if key == 'language':
                return translation['language']
            if key in translation['content']:
                return translation['content'][key]

    translation = translations[0]['content'].get(key)
    if translation is None:
        logger.warning(f"Missing translation for key '{key}' in language '{language_code}'.")

    return translation if translation else f"Translation missing for key: {key}"