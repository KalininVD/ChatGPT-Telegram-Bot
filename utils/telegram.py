# Import necessary modules, classes and functions
from telebot import TeleBot
from telebot.types import BotCommand, BotCommandScopeChat
from decimal import Decimal
from utils.yandexcloud import query_find, query_search, query_insert, query_update, query_delete

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
BASE_COMMANDS = [
    BotCommand('start', 'Get started with ChatGPT Telegram Bot'),
    BotCommand('help', 'Get help message of the bot'),
    BotCommand('language', 'Change the language for the bot'),
    BotCommand('budget', 'Check the remaining budget of the bot'),
]

# Define the commands for the users of the bot
USER_COMMANDS = BASE_COMMANDS + [
    BotCommand('reset', 'Start a new conversation'),
    BotCommand('summarize', 'Summarize the last conversation'),
]

# Define the commands for the admins of the bot
ADMIN_COMMANDS = USER_COMMANDS + [
    BotCommand('settings', 'Get the bot settings'),
]

# Define the commands for the owner of the bot
OWNER_COMMANDS = ADMIN_COMMANDS + [
    BotCommand('users', 'Manage users and admins of the bot'),
]

# Update the bot's commands for the specified user
def UpdateBotCommands(telegram_bot: TeleBot, chat_id: int, user_id: int, user_name: str):
    match GetCategory(user_id, user_name):
        case 'owner':
            telegram_bot.set_my_commands(scope=BotCommandScopeChat(chat_id), commands=OWNER_COMMANDS)
        case 'admin':
            telegram_bot.set_my_commands(scope=BotCommandScopeChat(chat_id), commands=ADMIN_COMMANDS)
        case 'user':
            telegram_bot.set_my_commands(scope=BotCommandScopeChat(chat_id), commands=USER_COMMANDS)
        case 'banned':
            telegram_bot.set_my_commands(scope=BotCommandScopeChat(chat_id), commands=BASE_COMMANDS)
        case _:
            telegram_bot.set_my_commands(scope=BotCommandScopeChat(chat_id), commands=BASE_COMMANDS)
            SetCategory(user_id, user_name, 'banned')

# Get the user's category
def GetCategory(user_id: int, user_name: str) -> str:
    user = GetUserInfo(user_id, user_name)
    
    if user:
        return user['info']['user_role']
    
    return 'unknown'

# Get the user's language
def GetLanguage(user_id: int, user_name: str) -> str:
    user = GetUserInfo(user_id, user_name)

    if user:
        return user['info']['language']
    
    return 'unknown'

# Get the user's chat model
def GetModel(user_id: int, user_name: str) -> str:
    user = GetUserInfo(user_id, user_name)

    if user:
        return user['info']['chat_model']
    
    return 'unknown'

# Get the user's remaining budget
def GetBudget(user_id: int, user_name: str) -> Decimal:
    user = GetUserInfo(user_id, user_name)

    if user:
        return user['info']['remaining_budget']
    
    return Decimal(0)

# Set the user's category
def SetCategory(user_id: int, user_name: str, user_role: str) -> bool:
    if user_role not in ('owner', 'admin', 'user', 'banned'):
        return False

    user = GetUserInfo(user_id, user_name)
    
    if user:
        response = query_update(
            user_id=Decimal(user_id),
            user_name=user_name,
            user_role=user_role,
            language=user['info']['language'],
            chat_model=user['info']['chat_model'],
            remaining_budget=user['info']['remaining_budget']
        )
    else:
        response = query_insert(
            user_id=Decimal(user_id),
            user_name=user_name,
            user_role=user_role,
            language="en",
            chat_model="gpt-3.5-turbo",
            remaining_budget=Decimal(0)
        )
    
    return response.get('ResponseMetadata', {}).get('HTTPStatusCode', None) == 200

# Set the user's language
def SetLanguage(user_id: int, user_name: str, language: str) -> bool:
    if language not in ('en', 'ru'):
        return False

    user = GetUserInfo(user_id, user_name)
    
    if user:
        response = query_update(
            user_id=Decimal(user_id),
            user_name=user_name,
            user_role=user['info']['user_role'],
            language=language,
            chat_model=user['info']['chat_model'],
            remaining_budget=user['info']['remaining_budget']
        )
    else:
        response = query_insert(
            user_id=Decimal(user_id),
            user_name=user_name,
            user_role="banned",
            language=language,
            chat_model="gpt-3.5-turbo",
            remaining_budget=Decimal(0)
        )
    
    return response.get('ResponseMetadata', {}).get('HTTPStatusCode', None) == 200

# Set the user's chat model
def SetModel(user_id: int, user_name: str, chat_model: str) -> bool:
    if chat_model not in ('gpt-3.5-turbo', 'gpt-4'):
        return False

    user = GetUserInfo(user_id, user_name)
    
    if user:
        response = query_update(
            user_id=Decimal(user_id),
            user_name=user_name,
            user_role=user['info']['user_role'],
            language=user['info']['language'],
            chat_model=chat_model,
            remaining_budget=user['info']['remaining_budget']
        )
    else:
        response = query_insert(
            user_id=Decimal(user_id),
            user_name=user_name,
            user_role="banned",
            language="en",
            chat_model=chat_model,
            remaining_budget=Decimal(0)
        )
    
    return response.get('ResponseMetadata', {}).get('HTTPStatusCode', None) == 200

# Set the user's remaining budget
def SetBudget(user_id: int, user_name: str, remaining_budget: Decimal) -> bool:
    if remaining_budget < 0:
        return False

    user = GetUserInfo(user_id, user_name)
    
    if user:
        response = query_update(
            user_id=Decimal(user_id),
            user_name=user_name,
            user_role=user['info']['user_role'],
            language=user['info']['language'],
            chat_model=user['info']['chat_model'],
            remaining_budget=remaining_budget
        )
    else:
        response = query_insert(
            user_id=Decimal(user_id),
            user_name=user_name,
            user_role="banned",
            language="en",
            chat_model="gpt-3.5-turbo",
            remaining_budget=remaining_budget
        )
    
    return response.get('ResponseMetadata', {}).get('HTTPStatusCode', None) == 200

# Get the information about the user from the database
def GetUserInfo(user_id: int, user_name: str) -> dict | None:
    response = query_find(Decimal(user_id), user_name)

    return response.get('Item', None)

# Get the information about the user from the list of users
def GetUserFromList(user_id: int, users: list[dict]) -> dict | None:
    for user in users:
        if user.get('user_id', None) == Decimal(user_id):
            return user
    return None

# Get the information about the users of the specified category from the database
def GetUsersByCategory(user_role: str) -> list[dict]:
    response = query_search(user_role)

    return response.get('Items', [])

# Delete the user's information from the database
def DeleteUserInfo(user_id: int, user_name: str) -> bool:
    response = query_delete(Decimal(user_id), user_name)

    return response.get('ResponseMetadata', {}).get('HTTPStatusCode', 200) == 200