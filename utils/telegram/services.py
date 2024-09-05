from logging import Logger
from decimal import Decimal
from telebot import TeleBot

import utils.telegram.commands
import utils.telegram.messages
import utils.telegram.callback_queries
from utils.users import UserInfo
from utils.yandexcloud.user_management import GetUserByID, AddNewUser, UpdateUserInfo

# Define environment variables
bot_token: str | None = None
owner_id: int | None = None

# Define services
logger: Logger

# Initialize environment variables
def InitEnvVars(telegram_bot_token: str | None = None, owner_telegram_id: str | None = None):
    if telegram_bot_token is None or owner_telegram_id is None:
        raise ValueError("Telegram Bot Token and Owner Telegram ID must be provided")

    global bot_token, owner_id
    
    bot_token = telegram_bot_token
    owner_id = int(owner_telegram_id)

# Setup logger
def SetupLogger(external_logger: Logger):
    global logger

    logger = external_logger
    utils.telegram.commands.logger = logger
    utils.telegram.messages.logger = logger
    utils.telegram.callback_queries.SetupLogger(logger)

# Initialize Telegram Bot
def InitBot() -> TeleBot:
    if bot_token is None:
        raise ValueError("Telegram Bot Token is not set")

    return TeleBot(bot_token, threaded=False)

# Setup the owner's information
def SetupOwnerInfo():
    if owner_id is None:
        raise ValueError("Owner Telegram ID is not set")

    AddNewUser(owner_id, 'owner', 0, 'owner')

# Get the user's information by ID
def GetUserInfoByID(user_id: int | Decimal, user_name: str = "unknown", chat_id: int = -1) -> UserInfo:
    user = GetUserByID(user_id)

    if user is None:
        logger.warning(f"User #{user_id} is not registered yet")

        user = AddNewUser(user_id, user_name, chat_id)
        
        if user is None:
            raise ValueError(f"Unable to register user #{user_id}")
        
        logger.info(f"Successfully registered user #{user_id}")
    
    user_info = UserInfo(user['info'])

    # Set the user's name and chat ID if the user is the owner but has not been registered fully yet
    if int(user_id) == owner_id and user_info['user_role'] == 'owner' and user_info['user_name'] == 'owner' and user_info['chat_id'] == 0:
        user_info['user_name'] = user_name
        user_info['chat_id'] = chat_id
        user_info['user_budget'] = Decimal('100') # Owner has unlimited budget, but Decimal('inf') is not supported by Yandex Cloud
        if UpdateUserInfo(user_id, user_info):
            logger.info(f"Successfully fully registered the owner of the bot (user #{user_id})")
        else:
            logger.warning(f"Failed to fully register the owner of the bot (user #{user_id})")
    
    return user_info