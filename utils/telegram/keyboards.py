from telebot.types import InlineKeyboardMarkup
from telebot.util import quick_markup

from utils.openai.models import (
    CHAT_MODELS, VISION_MODELS, IMAGE_MODELS,
    TRANSLATE_MODELS, STT_MODELS, TTS_MODELS,
)
from utils.openai.chat_model_params import TEMPERATURES, TOKEN_LIMITS
from utils.system_prompts import SYSTEM_PROMPTS
from utils.translations import GetTranslation as Translate, supported_languages
from utils.yandexcloud.user_management import GetUsersByCategory

# Generate the inline keyboard for managing the bot's language
def Language() -> InlineKeyboardMarkup:
    return quick_markup(
        dict(
            (Translate(language, 'language'), {'callback_data': f"language_{language}"}) for language in supported_languages
        ),
        row_width=2,
    )

# Generate the inline keyboard for managing the bot's settings
def Settings(language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        {
            Translate(language, 'button_model_chat'): {'callback_data': 'settings_model_chat'},
            Translate(language, 'button_model_vision'): {'callback_data': 'settings_model_vision'},
            Translate(language, 'button_model_image'): {'callback_data': 'settings_model_image'},
            Translate(language, 'button_model_translate'): {'callback_data': 'settings_model_translate'},
            Translate(language, 'button_model_transcribe'): {'callback_data': 'settings_model_transcribe'},
            Translate(language, 'button_model_syntesize'): {'callback_data': 'settings_model_syntesize'},
            Translate(language, 'button_temperature'): {'callback_data': 'settings_temperature'},
            Translate(language, 'button_token_limit'): {'callback_data': 'settings_token_limit'},
        },
        row_width=1,
    )

# Generate the inline keyboard for managing the bot's chat model
def SettingsModelChat(language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        dict(
            [(chat_model, {'callback_data': f"settings_model_chat_{chat_model}"}) for chat_model in CHAT_MODELS] +
            [(Translate(language, 'button_back'), {'callback_data': 'settings'})]
        ),
        row_width=1,
    )

# Generate the inline keyboard for managing the bot's vision model
def SettingsModelVision(language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        dict(
            [(vision_model, {'callback_data': f"settings_model_vision_{vision_model}"}) for vision_model in VISION_MODELS] +
            [(Translate(language, 'button_back'), {'callback_data': 'settings'})]
        ),
        row_width=1,
    )

# Generate the inline keyboard for managing the bot's image model
def SettingsModelImage(language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        dict(
            [(image_model, {'callback_data': f"settings_model_image_{image_model}"}) for image_model in IMAGE_MODELS] +
            [(Translate(language, 'button_back'), {'callback_data': 'settings'})]
        ),
        row_width=1,
    )

# Generate the inline keyboard for managing the bot's translate model
def SettingsModelTranslate(language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        dict(
            [(translate_model, {'callback_data': f"settings_model_translate_{translate_model}"}) for translate_model in TRANSLATE_MODELS] +
            [(Translate(language, 'button_back'), {'callback_data': 'settings'})]
        ),
        row_width=1,
    )

# Generate the inline keyboard for managing the bot's transcribe model
def SettingsModelTranscribe(language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        dict(
            [(transcribe_model, {'callback_data': f"settings_model_transcribe_{transcribe_model}"}) for transcribe_model in STT_MODELS] +
            [(Translate(language, 'button_back'), {'callback_data': 'settings'})]
        ),
        row_width=1,
    )

# Generate the inline keyboard for managing the bot's syntesize model
def SettingsModelSyntesize(language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        dict(
            [(syntesize_model, {'callback_data': f"settings_model_syntesize_{syntesize_model}"}) for syntesize_model in TTS_MODELS] +
            [(Translate(language, 'button_back'), {'callback_data': 'settings'})]
        ),
        row_width=1,
    )

# Generate the inline keyboard for managing the bot's chat model temperature
def SettingsTemperature(language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        dict(
            [(str(temperature), {'callback_data': f"settings_temperature_{temperature}"}) for temperature in TEMPERATURES] +
            [(Translate(language, 'button_back'), {'callback_data': 'settings'})]
        ),
        row_width=3,
    )

# Generate the inline keyboard for managing the chat model token limit
def SettingsTokenLimit(language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        dict(
            [(str(token_limit), {'callback_data': f"settings_token_limit_{token_limit}"}) for token_limit in TOKEN_LIMITS] +
            [(Translate(language, 'button_back'), {'callback_data': 'settings'})]
        ),
        row_width=2,
    )

# Generate the inline keyboard for managing the system prompt for the new conversation
def Reset(language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        dict(
            (prompt[language]['brief'], {'callback_data': f"reset_{prompt['en']['brief'].lower()}"}) for prompt in SYSTEM_PROMPTS
        ),
        row_width=1,
    )

# Generate the inline keyboard for managing all users of the bot
def Users(language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        {
            Translate(language, 'button_admins'): {'callback_data': 'manage_admins'},
            Translate(language, 'button_users'): {'callback_data': 'manage_users'},
            Translate(language, 'button_banned'): {'callback_data': 'manage_banned'},
        },
        row_width=1,
    )

# Generate the inline keyboard for managing the user's role
def UsersRole(user_id: int, language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        {
            Translate(language, 'button_role_admin'): {'callback_data': f"manage_role_admin_{user_id}"},
            Translate(language, 'button_role_user'): {'callback_data': f"manage_role_user_{user_id}"},
            Translate(language, 'button_role_banned'): {'callback_data': f"manage_role_banned_{user_id}"},
            Translate(language, 'button_delete'): {'callback_data': f"manage_delete_{user_id}"},
            Translate(language, 'button_back'): {'callback_data': f"manage_{user_id}"},
        },
        row_width=1,
    )

# Generate the inline keyboard for confirming deleting the banned user
def UsersDelete(user_id: int, language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        {
            Translate(language, 'button_yes'): {'callback_data': f"manage_remove_{user_id}"},
            Translate(language, 'button_no'): {'callback_data': f"manage_role_{user_id}"},
        },
        row_width=2,
    )

# Generate the inline keyboard for managing the user's language
def UsersLanguage(user_id: int, language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        dict(
            [(Translate(language, f"button_language_{lang}"), {'callback_data': f"manage_language_{lang}_{user_id}"}) for lang in supported_languages] +
            [(Translate(language, 'button_back'), {'callback_data': f"manage_{user_id}"})]
        ),
        row_width=2,
    )

# Generate the inline keyboard for managing the user's settings
def UsersSettings(user_id: int, language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        {
            Translate(language, 'button_model_chat'): {'callback_data': f"manage_model_chat_{user_id}"},
            Translate(language, 'button_model_vision'): {'callback_data': f"manage_model_vision_{user_id}"},
            Translate(language, 'button_model_image'): {'callback_data': f"manage_model_image_{user_id}"},
            Translate(language, 'button_model_translate'): {'callback_data': f"manage_model_translate_{user_id}"},
            Translate(language, 'button_model_transcribe'): {'callback_data': f"manage_model_transcribe_{user_id}"},
            Translate(language, 'button_model_syntesize'): {'callback_data': f"manage_model_syntesize_{user_id}"},
            Translate(language, 'button_temperature'): {'callback_data': f"manage_temperature_{user_id}"},
            Translate(language, 'button_token_limit'): {'callback_data': f"manage_token_limit_{user_id}"},
            Translate(language, 'button_back'): {'callback_data': f"manage_{user_id}"},
        },
        row_width=1,
    )

# Generate the inline keyboard for managing the user's chat model
def UsersModelChat(user_id: int, language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        dict(
            [(chat_model, {'callback_data': f"manage_model_chat_{chat_model}_{user_id}"}) for chat_model in CHAT_MODELS] +
            [(Translate(language, 'button_back'), {'callback_data': f"manage_settings_{user_id}"})]
        ),
        row_width=1,
    )

# Generate the inline keyboard for managing the user's vision model
def UsersModelVision(user_id: int, language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        dict(
            [(vision_model, {'callback_data': f"manage_model_vision_{vision_model}_{user_id}"}) for vision_model in VISION_MODELS] +
            [(Translate(language, 'button_back'), {'callback_data': f"manage_settings_{user_id}"})]
        ),
        row_width=1,
    )

# Generate the inline keyboard for managing the user's image model
def UsersModelImage(user_id: int, language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        dict(
            [(image_model, {'callback_data': f"manage_model_image_{image_model}_{user_id}"}) for image_model in IMAGE_MODELS] +
            [(Translate(language, 'button_back'), {'callback_data': f"manage_settings_{user_id}"})]
        ),
        row_width=1,
    )

# Generate the inline keyboard for managing the user's translate model
def UsersModelTranslate(user_id: int, language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        dict(
            [(translate_model, {'callback_data': f"manage_model_translate_{translate_model}_{user_id}"}) for translate_model in TRANSLATE_MODELS] +
            [(Translate(language, 'button_back'), {'callback_data': f"manage_settings_{user_id}"})]
        ),
        row_width=1,
    )

# Generate the inline keyboard for managing the user's transcribe model
def UsersModelTranscribe(user_id: int, language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        dict(
            [(transcribe_model, {'callback_data': f"manage_model_transcribe_{transcribe_model}_{user_id}"}) for transcribe_model in STT_MODELS] +
            [(Translate(language, 'button_back'), {'callback_data': f"manage_settings_{user_id}"})]
        ),
        row_width=1,
    )

# Generate the inline keyboard for managing the user's syntesize model
def UsersModelSyntesize(user_id: int, language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        dict(
            [(syntesize_model, {'callback_data': f"manage_model_syntesize_{syntesize_model}_{user_id}"}) for syntesize_model in TTS_MODELS] +
            [(Translate(language, 'button_back'), {'callback_data': f"manage_settings_{user_id}"})]
        ),
        row_width=1,
    )

# Generate the inline keyboard for managing the user's chat model temperature
def UsersTemperature(user_id: int, language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        dict(
            [(str(temperature), {'callback_data': f"manage_temperature_{temperature}_{user_id}"}) for temperature in TEMPERATURES] +
            [(Translate(language, 'button_back'), {'callback_data': f"manage_settings_{user_id}"})]
        ),
        row_width=3,
    )

# Generate the inline keyboard for managing the chat model token limit
def UsersTokenLimit(user_id: int, language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        dict(
            [(str(token_limit), {'callback_data': f"manage_token_limit_{token_limit}_{user_id}"}) for token_limit in TOKEN_LIMITS] +
            [(Translate(language, 'button_back'), {'callback_data': f"manage_settings_{user_id}"})]
        ),
        row_width=2,
    )

# Generate the inline keyboard for managing the user's remaining budget
def UsersBudget(user_id: int, language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        {
            Translate(language, 'button_increase'): {'callback_data': f"manage_budget_increase_{user_id}"},
            Translate(language, 'button_decrease'): {'callback_data': f"manage_budget_decrease_{user_id}"},
            Translate(language, 'button_back'): {'callback_data': f"manage_{user_id}"},
        },
        row_width=1,
    )

# Generate the inline keyboard for managing admins of the bot
def UsersAdmins(language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        dict(
            [(f"@{user['info']['user_name']}", {'callback_data': f"manage_{user['id']}"}) for user in GetUsersByCategory('admin')] +
            [(Translate(language, 'button_back'), {'callback_data': 'manage'})]
        ),
        row_width=1,
    )

# Generate the inline keyboard for managing users of the bot
def UsersUsers(language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        dict(
            [(f"@{user['info']['user_name']}", {'callback_data': f"manage_{user['id']}"}) for user in GetUsersByCategory('user')] +
            [(Translate(language, 'button_back'), {'callback_data': 'manage'})]
        ),
        row_width=1,
    )

# Generate the inline keyboard for managing banned users of the bot
def UsersBanned(language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        dict(
            [(f"@{user['info']['user_name']}", {'callback_data': f"manage_{user['id']}"}) for user in GetUsersByCategory('banned')] +
            [(Translate(language, 'button_back'), {'callback_data': 'manage'})]
        ),
        row_width=1,
    )

# Generate the inline keyboard for managing the admin
def UsersAdmin(user_id: int, language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        {
            Translate(language, 'button_role'): {'callback_data': f"manage_role_{user_id}"},
            Translate(language, 'button_language'): {'callback_data': f"manage_language_{user_id}"},
            Translate(language, 'button_settings'): {'callback_data': f"manage_settings_{user_id}"},
            Translate(language, 'button_budget'): {'callback_data': f"manage_budget_{user_id}"},
            Translate(language, 'button_back'): {'callback_data': 'manage_admins'},
        },
        row_width=1,
    )

# Generate the inline keyboard for managing the user
def UsersUser(user_id: int, language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        {
            Translate(language, 'button_role'): {'callback_data': f"manage_role_{user_id}"},
            Translate(language, 'button_language'): {'callback_data': f"manage_language_{user_id}"},
            Translate(language, 'button_settings'): {'callback_data': f"manage_settings_{user_id}"},
            Translate(language, 'button_budget'): {'callback_data': f"manage_budget_{user_id}"},
            Translate(language, 'button_back'): {'callback_data': 'manage_users'},
        },
        row_width=1,
    )

# Generate the inline keyboard for managing the banned user
def UsersBannedUser(user_id: int, language: str = 'en') -> InlineKeyboardMarkup:
    return quick_markup(
        {
            Translate(language, 'button_role'): {'callback_data': f"manage_role_{user_id}"},
            Translate(language, 'button_language'): {'callback_data': f"manage_language_{user_id}"},
            Translate(language, 'button_back'): {'callback_data': 'manage_banned'},
        },
        row_width=1,
    )