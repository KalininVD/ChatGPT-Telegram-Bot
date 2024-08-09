# Import necessary modules, classes and functions
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.telegram import GetUsersByCategory

# Generate the inline keyboard for managing the bot's language
def LanguageGeneral() -> InlineKeyboardMarkup:
    keyboard = [[]]

    keyboard[0].append(InlineKeyboardButton(text="English", callback_data="language_en"))
    keyboard[0].append(InlineKeyboardButton(text="Russian", callback_data="language_ru"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing the bot's settings
def Settings() -> InlineKeyboardMarkup:
    keyboard = [[]]

    keyboard[0].append(InlineKeyboardButton(text="Language", callback_data="settings_language"))
    keyboard[0].append(InlineKeyboardButton(text="Chat Model", callback_data="settings_model"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing the bot's language from the settings
def LanguageSettings() -> InlineKeyboardMarkup:
    keyboard = [[], []]

    keyboard[0].append(InlineKeyboardButton(text="English", callback_data="settings_language_en"))
    keyboard[0].append(InlineKeyboardButton(text="Russian", callback_data="settings_language_ru"))
    keyboard[1].append(InlineKeyboardButton(text="Back", callback_data="settings"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing the bot's chat model
def ModelSettings() -> InlineKeyboardMarkup:
    keyboard = [[], []]

    keyboard[0].append(InlineKeyboardButton(text="GPT-3.5-Turbo", callback_data="settings_model_gpt35"))
    keyboard[0].append(InlineKeyboardButton(text="GPT-4", callback_data="settings_model_gpt4"))
    keyboard[1].append(InlineKeyboardButton(text="Back", callback_data="settings"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing all users of the bot
def UserCategoties() -> InlineKeyboardMarkup:
    keyboard = [[], []]

    keyboard[0].append(InlineKeyboardButton(text="Admins", callback_data="manage_admins"))
    keyboard[0].append(InlineKeyboardButton(text="Users", callback_data="manage_users"))
    keyboard[1].append(InlineKeyboardButton(text="Banned Users", callback_data="manage_banned"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing admins of the bot
def Admins() -> InlineKeyboardMarkup:
    keyboard = [[]]

    for user in GetUsersByCategory('admin'):
        if len(keyboard[-1]) == 2:
            keyboard.append([])
        keyboard[-1].append(InlineKeyboardButton(text=f"@{user['info']['name']}", callback_data=f"manage_admin_{user['id']}"))
    
    if len(keyboard[-1]) == 2:
        keyboard.append([])
    keyboard[-1].append(InlineKeyboardButton(text="Back", callback_data="manage"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing users of the bot
def Users() -> InlineKeyboardMarkup:
    keyboard = [[]]

    for user in GetUsersByCategory('user'):
        if len(keyboard[-1]) == 2:
            keyboard.append([])
        keyboard[-1].append(InlineKeyboardButton(text=f"@{user['info']['name']}", callback_data=f"manage_user_{user['id']}"))
    
    if len(keyboard[-1]) == 2:
        keyboard.append([])
    keyboard[-1].append(InlineKeyboardButton(text="Back", callback_data="manage"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing banned users of the bot
def BannedUsers() -> InlineKeyboardMarkup:
    keyboard = [[]]

    for user in GetUsersByCategory('banned'):
        if len(keyboard[-1]) == 2:
            keyboard.append([])
        keyboard[-1].append(InlineKeyboardButton(text=f"@{user['info']['name']}", callback_data=f"manage_banned_{user['id']}"))
    
    if len(keyboard[-1]) == 2:
        keyboard.append([])
    keyboard[-1].append(InlineKeyboardButton(text="Back", callback_data="manage"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing the admin
def Admin(user_id: int) -> InlineKeyboardMarkup:
    keyboard = [[], []]

    keyboard[0].append(InlineKeyboardButton(text="Make User", callback_data=f"manage_role_user_{user_id}"))
    keyboard[0].append(InlineKeyboardButton(text="Make Banned", callback_data=f"manage_role_banned_{user_id}"))
    keyboard[1].append(InlineKeyboardButton(text="Delete Admin", callback_data=f"manage_delete_admin_{user_id}"))
    keyboard[1].append(InlineKeyboardButton(text="Back", callback_data="manage_admins"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing the user
def User(user_id: int) -> InlineKeyboardMarkup:
    keyboard = [[], [], [], []]

    keyboard[0].append(InlineKeyboardButton(text="Language", callback_data=f"manage_language_{user_id}"))
    keyboard[0].append(InlineKeyboardButton(text="Chat Model", callback_data=f"manage_model_{user_id}"))
    keyboard[1].append(InlineKeyboardButton(text="Remaining Budget", callback_data=f"manage_budget_{user_id}"))
    keyboard[1].append(InlineKeyboardButton(text="Make Admin", callback_data=f"manage_role_admin_{user_id}"))
    keyboard[2].append(InlineKeyboardButton(text="Make Banned", callback_data=f"manage_role_banned_{user_id}"))
    keyboard[2].append(InlineKeyboardButton(text="Delete User", callback_data=f"manage_delete_user_{user_id}"))
    keyboard[3].append(InlineKeyboardButton(text="Back", callback_data="manage_users"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing the banned user
def BannedUser(user_id: int) -> InlineKeyboardMarkup:
    keyboard = [[], []]

    keyboard[0].append(InlineKeyboardButton(text="Make Admin", callback_data=f"manage_role_admin_{user_id}"))
    keyboard[0].append(InlineKeyboardButton(text="Make User", callback_data=f"manage_role_user_{user_id}"))
    keyboard[1].append(InlineKeyboardButton(text="Delete Banned User", callback_data=f"manage_delete_banned_{user_id}"))
    keyboard[1].append(InlineKeyboardButton(text="Back", callback_data="manage_banned"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing the user's language
def Language(user_id: int) -> InlineKeyboardMarkup:
    keyboard = [[], []]

    keyboard[0].append(InlineKeyboardButton(text="English", callback_data=f"manage_language_en_{user_id}"))
    keyboard[0].append(InlineKeyboardButton(text="Russian", callback_data=f"manage_language_ru_{user_id}"))
    keyboard[1].append(InlineKeyboardButton(text="Leave unchanged", callback_data=f"manage_user_{user_id}"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing the user's chat model
def Model(user_id: int) -> InlineKeyboardMarkup:
    keyboard = [[], []]

    keyboard[0].append(InlineKeyboardButton(text="GPT-3.5-Turbo", callback_data=f"manage_model_gpt35_{user_id}"))
    keyboard[0].append(InlineKeyboardButton(text="GPT-4", callback_data=f"manage_model_gpt4_{user_id}"))
    keyboard[1].append(InlineKeyboardButton(text="Leave unchanged", callback_data=f"manage_user_{user_id}"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for managing the user's remaining budget
def Budget(user_id: int) -> InlineKeyboardMarkup:
    keyboard = [[], []]

    keyboard[0].append(InlineKeyboardButton(text="Add 0.1$", callback_data=f"manage_budget_increase_{user_id}"))
    keyboard[0].append(InlineKeyboardButton(text="Remove 0.1$", callback_data=f"manage_budget_decrease_{user_id}"))
    keyboard[1].append(InlineKeyboardButton(text="Leave unchanged", callback_data=f"manage_user_{user_id}"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for confirming deleting the admin
def DeleteAdmin(user_id: int) -> InlineKeyboardMarkup:
    keyboard = [[]]

    keyboard[0].append(InlineKeyboardButton(text="Yes", callback_data=f"manage_remove_admin_{user_id}"))
    keyboard[0].append(InlineKeyboardButton(text="No", callback_data=f"manage_admin_{user_id}"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for confirming deleting the user
def DeleteUser(user_id: int) -> InlineKeyboardMarkup:
    keyboard = [[]]

    keyboard[0].append(InlineKeyboardButton(text="Yes", callback_data=f"manage_remove_user_{user_id}"))
    keyboard[0].append(InlineKeyboardButton(text="No", callback_data=f"manage_user_{user_id}"))

    return InlineKeyboardMarkup(keyboard)

# Generate the inline keyboard for confirming deleting the banned user
def DeleteBanned(user_id: int) -> InlineKeyboardMarkup:
    keyboard = [[]]

    keyboard[0].append(InlineKeyboardButton(text="Yes", callback_data=f"manage_remove_banned_{user_id}"))
    keyboard[0].append(InlineKeyboardButton(text="No", callback_data=f"manage_banned_{user_id}"))

    return InlineKeyboardMarkup(keyboard)