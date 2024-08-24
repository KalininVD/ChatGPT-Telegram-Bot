# Import necessary modules, classes and functions
from telebot import TeleBot
from telebot.types import BotCommand, BotCommandScopeChat
from decimal import Decimal
from utils.yandexcloud import query_find, query_search, query_insert, query_update, query_delete
from utils.openai import CHAT_MODELS
from utils.translations import get_translation as Translate

# Define environment variables
TELEGRAM_BOT_TOKEN: str | None = None
OWNER_TELEGRAM_ID: int | None = None
OWNER_TELEGRAM_NAME: str | None = None

# Initialize environment variables
def InitEnvVars(env_vars: dict):
    global TELEGRAM_BOT_TOKEN, OWNER_TELEGRAM_ID, OWNER_TELEGRAM_NAME
    
    TELEGRAM_BOT_TOKEN = env_vars.get('TELEGRAM_BOT_TOKEN')
    OWNER_TELEGRAM_ID = env_vars.get('OWNER_TELEGRAM_ID')
    OWNER_TELEGRAM_NAME = env_vars.get('OWNER_TELEGRAM_NAME')

# Define base commands for the bot
def GetBaseCommands(language: str = "en") -> list[BotCommand]:
    return [
        BotCommand('start', Translate(language, "start_command_description")),
        BotCommand('help', Translate(language, "help_command_description")),
        BotCommand('language', Translate(language, "language_command_description")),
        BotCommand('budget', Translate(language, "budget_command_description")),
    ]

# Define the commands for the users of the bot
def GetUserCommands(language: str = "en") -> list[BotCommand]:
    return GetBaseCommands(language) + [
        BotCommand('reset', Translate(language, "reset_command_description")),
        BotCommand('summarize', Translate(language, "summarize_command_description")),
    ]

# Define the commands for the admins of the bot
def GetAdminCommands(language: str = "en") -> list[BotCommand]:
    return GetUserCommands(language) + [
        BotCommand('settings', Translate(language, "settings_command_description")),
    ]

# Define the commands for the owner of the bot
def GetOwnerCommands(language: str = "en") -> list[BotCommand]:
    return GetAdminCommands(language) + [
        BotCommand('users', Translate(language, "users_command_description")),
    ]

# Update the bot's commands for the specified user
def UpdateBotCommands(telegram_bot: TeleBot, chat_id: int, user_id: int):
    lang = GetLanguage(user_id)

    match GetCategory(user_id):
        case 'owner':
            telegram_bot.set_my_commands(scope=BotCommandScopeChat(chat_id), commands=GetOwnerCommands(lang))
        case 'admin':
            telegram_bot.set_my_commands(scope=BotCommandScopeChat(chat_id), commands=GetAdminCommands(lang))
        case 'user':
            telegram_bot.set_my_commands(scope=BotCommandScopeChat(chat_id), commands=GetUserCommands(lang))
        case 'banned':
            telegram_bot.set_my_commands(scope=BotCommandScopeChat(chat_id), commands=GetBaseCommands(lang))
        case _:
            telegram_bot.set_my_commands(scope=BotCommandScopeChat(chat_id), commands=GetBaseCommands(lang))
            SetCategory(user_id, 'banned')
            SetName(user_id, telegram_bot.get_chat_member(chat_id, user_id).user.username)

# Get the user's name
def GetName(user_id: int) -> str:
    user = GetUserInfo(user_id)

    if user:
        return user['info']['name']
    
    return 'unknown'

# Get the user's category
def GetCategory(user_id: int) -> str:
    user = GetUserInfo(user_id)
    
    if user:
        return user['info']['role']
    
    return 'unknown'

# Get the user's language
def GetLanguage(user_id: int) -> str:
    user = GetUserInfo(user_id)

    if user:
        return user['info']['language']
    
    return 'unknown'

# Get the user's chat model
def GetModel(user_id: int) -> str:
    user = GetUserInfo(user_id)

    if user:
        return user['info']['model']
    
    return 'unknown'

# Get the user's remaining budget
def GetBudget(user_id: int) -> Decimal:
    user = GetUserInfo(user_id)

    if user:
        return user['info']['budget']
    
    return Decimal(0)

# Set the user's name
def SetName(id: int, name: str) -> bool:
    if len(name) > 32:
        return False

    user = GetUserInfo(id)
    
    if user:
        response = query_update(
            id=Decimal(id),
            name=name,
            role=user['info']['role'],
            language=user['info']['language'],
            model=user['info']['model'],
            budget=user['info']['budget']
        )
    else:
        response = query_insert(
            id=Decimal(id),
            name=name,
            role="banned",
            language="en",
            model="gpt-4o-mini",
            remaining_budget=Decimal(0)
        )
    
    return response.get('ResponseMetadata', {}).get('HTTPStatusCode', None) == 200

# Set the user's category
def SetCategory(id: int, role: str) -> bool:
    if role not in ('owner', 'admin', 'user', 'banned'):
        return False

    user = GetUserInfo(id)
    
    if user:
        response = query_update(
            id=Decimal(id),
            name=user['info']['name'],
            role=role,
            language=user['info']['language'],
            model=user['info']['model'],
            budget=user['info']['budget']
        )
    else:
        response = query_insert(
            id=Decimal(id),
            name="unknown",
            role=role,
            language="en",
            model="gpt-4o-mini",
            budget=Decimal(0)
        )
    
    return response.get('ResponseMetadata', {}).get('HTTPStatusCode', None) == 200

# Set the user's language
def SetLanguage(id: int, language: str) -> bool:
    if language not in ('en', 'ru'):
        return False

    user = GetUserInfo(id)
    
    if user:
        response = query_update(
            id=Decimal(id),
            name=user['info']['name'],
            role=user['info']['role'],
            language=language,
            model=user['info']['model'],
            budget=user['info']['budget']
        )
    else:
        response = query_insert(
            id=Decimal(id),
            name="unknown",
            role="banned",
            language=language,
            model="gpt-4o-mini",
            budget=Decimal(0)
        )
    
    return response.get('ResponseMetadata', {}).get('HTTPStatusCode', None) == 200

# Set the user's chat model
def SetModel(id: int, model: str) -> bool:
    if model not in CHAT_MODELS:
        return False

    user = GetUserInfo(id)
    
    if user:
        response = query_update(
            id=Decimal(id),
            name=user['info']['name'],
            role=user['info']['role'],
            language=user['info']['language'],
            model=model,
            budget=user['info']['budget']
        )
    else:
        response = query_insert(
            id=Decimal(id),
            name="unknown",
            role="banned",
            language="en",
            model=model,
            budget=Decimal(0)
        )
    
    return response.get('ResponseMetadata', {}).get('HTTPStatusCode', None) == 200

# Set the user's remaining budget
def SetBudget(id: int, budget: Decimal) -> bool:
    user = GetUserInfo(id)
    
    if user:
        response = query_update(
            id=Decimal(id),
            name=user['info']['name'],
            role=user['info']['role'],
            language=user['info']['language'],
            model=user['info']['model'],
            budget=budget
        )
    else:
        response = query_insert(
            id=Decimal(id),
            name="unknown",
            role="banned",
            language="en",
            model="gpt-4o-mini",
            budget=budget
        )
    
    return response.get('ResponseMetadata', {}).get('HTTPStatusCode', None) == 200

# Get the information about the user from the database
def GetUserInfo(user_id: int) -> dict | None:
    response = query_find(Decimal(user_id))

    return response.get('Item', None)

# Get the information about the user from the list of users
def GetUserFromList(user_id: int, users: list[dict]) -> dict | None:
    for user in users:
        if user.get('id', None) == Decimal(user_id):
            return user
    return None

# Get the information about the users of the specified category from the database
def GetUsersByCategory(user_role: str) -> list[dict]:
    response = query_search(user_role)

    return response.get('Items', [])

# Delete the user's information from the database
def DeleteUserInfo(user_id: int) -> bool:
    response = query_delete(Decimal(user_id))

    return response.get('ResponseMetadata', {}).get('HTTPStatusCode', 200) == 200