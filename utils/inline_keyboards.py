# Import necessary modules, classes and functions
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.telegram import GetUsersByCategory
from utils.translations import get_translation as Translate
from utils.openai import CHAT_MODELS

# Generate the inline keyboard for managing the bot's language
def LanguageGeneral() -> InlineKeyboardMarkup:
    keyboard = [[]]

    keyboard[0].append(InlineKeyboardButton(text=Translate("en", "language"), callback_data="language_en"))
    keyboard[0].append(InlineKeyboardButton(text=Translate("ru", "language"), callback_data="language_ru"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing the bot's settings
def Settings(language: str = "en") -> InlineKeyboardMarkup:
    keyboard = [[]]

    keyboard[0].append(InlineKeyboardButton(text=Translate(language, "language_button"), callback_data="settings_language"))
    keyboard[0].append(InlineKeyboardButton(text=Translate(language, "model_button"), callback_data="settings_model"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing the bot's language from the settings
def LanguageSettings(language: str = "en") -> InlineKeyboardMarkup:
    keyboard = [[], []]

    keyboard[0].append(InlineKeyboardButton(text=Translate(language, "language_button_en"), callback_data="settings_language_en"))
    keyboard[0].append(InlineKeyboardButton(text=Translate(language, "language_button_ru"), callback_data="settings_language_ru"))
    keyboard[1].append(InlineKeyboardButton(text=Translate(language, "back_button"), callback_data="settings"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing the bot's chat model
def ModelSettings(language: str = "en") -> InlineKeyboardMarkup:
    keyboard = [[]]

    for chat_model in CHAT_MODELS:
        if len(keyboard[-1]) == 2:
            keyboard.append([])
        
        keyboard[-1].append(InlineKeyboardButton(text=chat_model, callback_data=f"settings_model_{chat_model}"))

    if len(keyboard[-1]) == 2:
        keyboard.append([])
    keyboard[-1].append(InlineKeyboardButton(text=Translate(language, "back_button"), callback_data="settings"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing all users of the bot
def UserCategoties(language: str = "en") -> InlineKeyboardMarkup:
    keyboard = [[], []]

    keyboard[0].append(InlineKeyboardButton(text=Translate(language, "admins"), callback_data="manage_admins"))
    keyboard[0].append(InlineKeyboardButton(text=Translate(language, "users"), callback_data="manage_users"))
    keyboard[1].append(InlineKeyboardButton(text=Translate(language, "banned_users"), callback_data="manage_banned"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing admins of the bot
def Admins(language: str = "en") -> InlineKeyboardMarkup:
    keyboard = [[]]

    for user in GetUsersByCategory('admin'):
        if len(keyboard[-1]) == 2:
            keyboard.append([])
        keyboard[-1].append(InlineKeyboardButton(text=f"@{user['info']['name']}", callback_data=f"manage_admin_{user['id']}"))
    
    if len(keyboard[-1]) == 2:
        keyboard.append([])
    keyboard[-1].append(InlineKeyboardButton(text=Translate(language, "back_button"), callback_data="manage"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing users of the bot
def Users(language: str = "en") -> InlineKeyboardMarkup:
    keyboard = [[]]

    for user in GetUsersByCategory('user'):
        if len(keyboard[-1]) == 2:
            keyboard.append([])
        keyboard[-1].append(InlineKeyboardButton(text=f"@{user['info']['name']}", callback_data=f"manage_user_{user['id']}"))
    
    if len(keyboard[-1]) == 2:
        keyboard.append([])
    keyboard[-1].append(InlineKeyboardButton(text=Translate(language, "back_button"), callback_data="manage"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing banned users of the bot
def BannedUsers(language: str = "en") -> InlineKeyboardMarkup:
    keyboard = [[]]

    for user in GetUsersByCategory('banned'):
        if len(keyboard[-1]) == 2:
            keyboard.append([])
        keyboard[-1].append(InlineKeyboardButton(text=f"@{user['info']['name']}", callback_data=f"manage_banned_{user['id']}"))
    
    if len(keyboard[-1]) == 2:
        keyboard.append([])
    keyboard[-1].append(InlineKeyboardButton(text=Translate(language, "back_button"), callback_data="manage"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing the admin
def Admin(user_id: int, language: str = "en") -> InlineKeyboardMarkup:
    keyboard = [[], []]

    keyboard[0].append(InlineKeyboardButton(text=Translate(language, "make_user"), callback_data=f"manage_role_user_{user_id}"))
    keyboard[0].append(InlineKeyboardButton(text=Translate(language, "make_banned"), callback_data=f"manage_role_banned_{user_id}"))
    keyboard[1].append(InlineKeyboardButton(text=Translate(language, "delete_admin"), callback_data=f"manage_delete_admin_{user_id}"))
    keyboard[1].append(InlineKeyboardButton(text=Translate(language, "back_button"), callback_data="manage_admins"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing the user
def User(user_id: int, language: str = "en") -> InlineKeyboardMarkup:
    keyboard = [[], [], [], []]

    keyboard[0].append(InlineKeyboardButton(text=Translate(language, "language_button"), callback_data=f"manage_language_{user_id}"))
    keyboard[0].append(InlineKeyboardButton(text=Translate(language, "model_button"), callback_data=f"manage_model_{user_id}"))
    keyboard[1].append(InlineKeyboardButton(text=Translate(language, "budget_button"), callback_data=f"manage_budget_{user_id}"))
    keyboard[1].append(InlineKeyboardButton(text=Translate(language, "make_admin"), callback_data=f"manage_role_admin_{user_id}"))
    keyboard[2].append(InlineKeyboardButton(text=Translate(language, "make_banned"), callback_data=f"manage_role_banned_{user_id}"))
    keyboard[2].append(InlineKeyboardButton(text=Translate(language, "delete_user"), callback_data=f"manage_delete_user_{user_id}"))
    keyboard[3].append(InlineKeyboardButton(text=Translate(language, "back_button"), callback_data="manage_users"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing the banned user
def Banned(user_id: int, language: str = "en") -> InlineKeyboardMarkup:
    keyboard = [[], []]

    keyboard[0].append(InlineKeyboardButton(text=Translate(language, "make_admin"), callback_data=f"manage_role_admin_{user_id}"))
    keyboard[0].append(InlineKeyboardButton(text=Translate(language, "make_user"), callback_data=f"manage_role_user_{user_id}"))
    keyboard[1].append(InlineKeyboardButton(text=Translate(language, "delete_banned"), callback_data=f"manage_delete_banned_{user_id}"))
    keyboard[1].append(InlineKeyboardButton(text=Translate(language, "back_button"), callback_data="manage_banned"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing the user's language
def Language(user_id: int, language: str = "en") -> InlineKeyboardMarkup:
    keyboard = [[], []]

    keyboard[0].append(InlineKeyboardButton(text=Translate(language, "language_button_en"), callback_data=f"manage_language_en_{user_id}"))
    keyboard[0].append(InlineKeyboardButton(text=Translate(language, "language_button_ru"), callback_data=f"manage_language_ru_{user_id}"))
    keyboard[1].append(InlineKeyboardButton(text=Translate(language, "back_button"), callback_data=f"manage_user_{user_id}"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing the user's chat model
def Model(user_id: int, language: str = "en") -> InlineKeyboardMarkup:
    keyboard = [[]]

    for chat_model in CHAT_MODELS:
        if len(keyboard[-1]) == 2:
            keyboard.append([])
        
        keyboard[-1].append(InlineKeyboardButton(text=chat_model, callback_data=f"manage_model_{chat_model}_{user_id}"))
    
    if len(keyboard[-1]) == 2:
        keyboard.append([])
    keyboard[-1].append(InlineKeyboardButton(text=Translate(language, "back_button"), callback_data=f"manage_user_{user_id}"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing the user's remaining budget
def Budget(user_id: int, language: str = "en") -> InlineKeyboardMarkup:
    keyboard = [[], []]

    keyboard[0].append(InlineKeyboardButton(text=Translate(language, "budget_increase"), callback_data=f"manage_budget_increase_{user_id}"))
    keyboard[0].append(InlineKeyboardButton(text=Translate(language, "budget_decrease"), callback_data=f"manage_budget_decrease_{user_id}"))
    keyboard[1].append(InlineKeyboardButton(text=Translate(language, "back_button"), callback_data=f"manage_user_{user_id}"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for confirming deleting the admin
def DeleteAdmin(user_id: int, language: str = "en") -> InlineKeyboardMarkup:
    keyboard = [[]]

    keyboard[0].append(InlineKeyboardButton(text=Translate(language, "yes_button"), callback_data=f"manage_remove_admin_{user_id}"))
    keyboard[0].append(InlineKeyboardButton(text=Translate(language, "no_button"), callback_data=f"manage_admin_{user_id}"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for confirming deleting the user
def DeleteUser(user_id: int, language: str = "en") -> InlineKeyboardMarkup:
    keyboard = [[]]

    keyboard[0].append(InlineKeyboardButton(text=Translate(language, "yes_button"), callback_data=f"manage_remove_user_{user_id}"))
    keyboard[0].append(InlineKeyboardButton(text=Translate(language, "no_button"), callback_data=f"manage_user_{user_id}"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for confirming deleting the banned user
def DeleteBanned(user_id: int, language: str = "en") -> InlineKeyboardMarkup:
    keyboard = [[]]

    keyboard[0].append(InlineKeyboardButton(text=Translate(language, "yes_button"), callback_data=f"manage_remove_banned_{user_id}"))
    keyboard[0].append(InlineKeyboardButton(text=Translate(language, "no_button"), callback_data=f"manage_banned_{user_id}"))

    return InlineKeyboardMarkup(keyboard)