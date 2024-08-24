# Import necessary modules
from os import path
import json

# Get the absolute path to the translations.json file
filepath = path.abspath(path.join(path.dirname(__file__), "..", "translations.json"))

# Load translations from the JSON file
translations = json.load(open(filepath))

# Retrieve message based on user language
def get_translation(language_code: str, key: str) -> str:
    for translation in translations:
        if translation['code'] == language_code:
            if key == 'language':
                return translation['language']
            if key in translation['content']:
                return translation['content'][key]
    
    return translations[0]['content'][key]