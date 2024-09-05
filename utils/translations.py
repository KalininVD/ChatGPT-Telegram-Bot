import json
from logging import Logger
from os import path

# Define services
logger: Logger
translations: dict[str, dict[str, str]] = {}
supported_languages: dict[str, str] = {}

# Load translations from the JSON file
def LoadTranslations():
    filepath = path.abspath(path.join(path.dirname(__file__), "..", "translations.json"))

    for translation in json.load(open(filepath, encoding='utf-8')):
        code = translation['code']
        language = translation['language']
        content = translation['content']

        translations[code] = dict(
            (message, content[message]) for message in content
        )

        supported_languages[code] = language

    logger.info(f"Successfully loaded {len(translations)} translations from file {filepath}")

# Get the message translation based on user language
def GetTranslation(language: str, message: str) -> str:
    if language not in supported_languages:
        logger.warning(f"Language '{language}' is not supported yet. Using 'en' instead.")
        language = 'en'

    if message == 'language':
        return supported_languages[language]

    translation = translations[language].get(message, None)

    if translation is None:
        logger.warning(f"Missing translation for message '{message}' in language '{language}'.")
        translation = f"No translation found for message: {message}"

    return translation