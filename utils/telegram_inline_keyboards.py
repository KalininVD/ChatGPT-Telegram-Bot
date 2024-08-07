# Import necessary modules, classes and functions
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.telegram import GetUsersByCategory

# Generate the inline keyboard for managing all users of the bot
def GenKBUserCategoties() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    admins = InlineKeyboardButton(text="Admins", callback_data="manage_admins")
    users = InlineKeyboardButton(text="Users", callback_data="manage_users")
    banned_users = InlineKeyboardButton(text="Banned Users", callback_data="manage_banned")

    keyboard.add(admins, users, banned_users)

    return keyboard

# Generate the inline keyboard for managing admins of the bot
def GenKBAdmins() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    for user in GetUsersByCategory('admin'):
        keyboard.add(InlineKeyboardButton(text=user['user_name'], callback_data=f"manage_admin_{user['user_id']}"))
    
    keyboard.add(InlineKeyboardButton(text="Back", callback_data="manage_bot"))

    return keyboard

# Generate the inline keyboard for managing users of the bot
def GenKBUsers() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    for user in GetUsersByCategory('user'):
        keyboard.add(InlineKeyboardButton(text=user['user_name'], callback_data=f"manage_user_{user['user_id']}"))
    
    keyboard.add(InlineKeyboardButton(text="Back", callback_data="manage_bot"))

    return keyboard

# Generate the inline keyboard for managing banned users of the bot
def GenKBBannedUsers() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    for user in GetUsersByCategory('banned'):
        keyboard.add(InlineKeyboardButton(text=user['user_name'], callback_data=f"manage_banned_{user['user_id']}"))
    
    keyboard.add(InlineKeyboardButton(text="Back", callback_data="manage_bot"))

    return keyboard

# Generate the inline keyboard for managing the admin
def GenKBAdmin(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    keyboard.add(InlineKeyboardButton(text="Make User", callback_data=f"change_role_user_{user_id}"))
    keyboard.add(InlineKeyboardButton(text="Make Banned", callback_data=f"change_role_banned_{user_id}"))
    keyboard.add(InlineKeyboardButton(text="Delete Admin", callback_data=f"delete_admin_{user_id}"))

    keyboard.add(InlineKeyboardButton(text="Back", callback_data="manage_admins"))

    return keyboard

# Generate the inline keyboard for managing the user
def GenKBUser(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    keyboard.add(InlineKeyboardButton(text="Language", callback_data=f"manage_language_{user_id}"))
    keyboard.add(InlineKeyboardButton(text="Chat Model", callback_data=f"manage_model_{user_id}"))
    keyboard.add(InlineKeyboardButton(text="Remaining Budget", callback_data=f"manage_budget_{user_id}"))

    keyboard.add(InlineKeyboardButton(text="Make Admin", callback_data=f"change_role_admin_{user_id}"))
    keyboard.add(InlineKeyboardButton(text="Make Banned", callback_data=f"change_role_banned_{user_id}"))
    keyboard.add(InlineKeyboardButton(text="Delete User", callback_data=f"delete_user_{user_id}"))

    keyboard.add(InlineKeyboardButton(text="Back", callback_data="manage_users"))

    return keyboard

# Generate the inline keyboard for managing the banned user
def GenKBBanned(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    keyboard.add(InlineKeyboardButton(text="Make Admin", callback_data=f"change_role_admin_{user_id}"))
    keyboard.add(InlineKeyboardButton(text="Make User", callback_data=f"change_role_user_{user_id}"))
    keyboard.add(InlineKeyboardButton(text="Delete Banned User", callback_data=f"delete_banned_{user_id}"))

    keyboard.add(InlineKeyboardButton(text="Back", callback_data="manage_banned"))

    return keyboard

# Generate the inline keyboard for managing the user's language
def GenKBLanguage(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    keyboard.add(InlineKeyboardButton(text="English", callback_data=f"change_language_en_{user_id}"))
    keyboard.add(InlineKeyboardButton(text="Russian", callback_data=f"change_language_ru_{user_id}"))
    keyboard.add(InlineKeyboardButton(text="Leave unchanged", callback_data=f"manage_user_{user_id}"))

    return keyboard

# Generate the inline keyboard for managing the user's chat model
def GenKBModel(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    keyboard.add(InlineKeyboardButton(text="GPT-3.5-Turbo", callback_data=f"change_model_gpt35_{user_id}"))
    keyboard.add(InlineKeyboardButton(text="GPT-4", callback_data=f"change_model_gpt4_{user_id}"))
    keyboard.add(InlineKeyboardButton(text="Leave unchanged", callback_data=f"manage_user_{user_id}"))

    return keyboard

# Generate the inline keyboard for managing the user's remaining budget
def GenKBBudget(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    keyboard.add(InlineKeyboardButton(text="Add 0.1$", callback_data=f"change_budget_plus_{user_id}"))
    keyboard.add(InlineKeyboardButton(text="Remove 0.1$", callback_data=f"change_budget_minus_{user_id}"))
    keyboard.add(InlineKeyboardButton(text="Leave unchanged", callback_data=f"manage_user_{user_id}"))

    return keyboard

# Generate the inline keyboard for confirming deleting the admin
def GenKBDeleteAdmin(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    keyboard.add(InlineKeyboardButton(text="Yes", callback_data=f"delete_confirmed_{user_id}"))
    keyboard.add(InlineKeyboardButton(text="No", callback_data=f"manage_admin_{user_id}"))

    return keyboard

# Generate the inline keyboard for confirming deleting the user
def GenKBDeleteUser(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    keyboard.add(InlineKeyboardButton(text="Yes", callback_data=f"delete_confirmed_{user_id}"))
    keyboard.add(InlineKeyboardButton(text="No", callback_data=f"manage_user_{user_id}"))

    return keyboard

# Generate the inline keyboard for confirming deleting the banned user
def GenKBDeleteBanned(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    keyboard.add(InlineKeyboardButton(text="Yes", callback_data=f"delete_confirmed_{user_id}"))
    keyboard.add(InlineKeyboardButton(text="No", callback_data=f"manage_banned_{user_id}"))

    return keyboard