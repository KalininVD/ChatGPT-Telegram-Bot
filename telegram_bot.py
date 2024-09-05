import logging
import telebot
from logging import Logger, Formatter
from telebot import TeleBot
from telebot.types import Update, Message, CallbackQuery

import utils.translations
import utils.telegram.services, utils.yandexcloud.services, utils.openai.services, utils.plugins.services
import utils.openai.helper
from utils.telegram.services import GetUserInfoByID
from utils.telegram.commands import (
    UpdateBotCommands, GetBaseCommands,
    HandleDisallowedCommand, HandleUnknownCommand,
    Start, Help, Language, Budget, Reset, Summarize, Settings, Users
)
from utils.telegram.messages import (
    HandleUnknownMessage, HandleDisallowedMessage,
    HandleTextMessage, HandlePhotoMessage,
    HandleAudioMessage, HandleVoiceMessage,
    HandleVideoMessage, HandleVideoNoteMessage,
    HandleDocumentMessage, HandleDiceMessage
)
from utils.telegram.callback_queries import (
    HandleLanguageCallbackQuery, HandleSettingsCallbackQuery, HandleResetCallbackQuery,
    HandleManagementCallbackQuery, HandleUnknownCallbackQuery,
)

# Define services
logger: Logger
bot: TeleBot

# Setup logger
def SetupLogger():
    global logger

    logger = telebot.logger
    logger.setLevel(logging.INFO)
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    formatter = Formatter(log_format)

    for handler in logger.handlers:
        handler.setFormatter(formatter)

    utils.translations.logger = logger
    utils.yandexcloud.services.SetupLogger(logger)
    utils.openai.services.SetupLogger(logger)
    utils.telegram.services.SetupLogger(logger)

# Initialize environment variables for all services
def InitEnvVars(yc_access_key_id: str | None = None, yc_secret_access_key: str | None = None, yc_docapi_endpoint: str | None = None,
                telegram_bot_token: str | None = None, owner_telegram_id: str | None = None,
                openai_api_key: str | None = None, openai_proxy: str | None = None,
                wolfram_api_key: str | None = None, duckduckgo_safesearch: str | None = None, worldtime_default_timezone: str | None = None):
    
    utils.yandexcloud.services.InitEnvVars(
        yc_access_key_id=yc_access_key_id,
        yc_secret_access_key=yc_secret_access_key,
        yc_docapi_endpoint=yc_docapi_endpoint,
    )

    utils.telegram.services.InitEnvVars(
        telegram_bot_token=telegram_bot_token,
        owner_telegram_id=owner_telegram_id,
    )

    utils.openai.services.InitEnvVars(
        openai_api_key=openai_api_key,
        openai_proxy=openai_proxy,
    )

    utils.plugins.services.InitEnvVars(
        wolfram_api_key=wolfram_api_key,
        duckduckgo_safesearch=duckduckgo_safesearch,
        worldtime_default_timezone=worldtime_default_timezone,
    )

# Initialize Telegram Bot
def InitBot():
    try:
        global bot

        bot = utils.telegram.services.InitBot()

        utils.translations.LoadTranslations()
        
        bot.set_my_commands(commands=GetBaseCommands())

        bot.register_message_handler(
            callback=HandleCommand,
            func=lambda message: True,
            commands=['start', 'help', 'language', 'budget', 'reset', 'summarize', 'settings', 'users'],
        )

        bot.register_message_handler(
            callback=HandleMessage,
            func=lambda message: True,
            content_types=['animation', 'audio', 'contact', 'dice', 'document', 'location', 'photo', 'poll', 'sticker', 'text', 'venue', 'video', 'video_note', 'voice'],
        )

        bot.register_callback_query_handler(
            callback=HandleCallbackQuery,
            func=lambda call: True,
        )

        utils.yandexcloud.services.InitServices()
        utils.telegram.services.SetupOwnerInfo()
        utils.openai.helper.InitHelper()

        logger.info("Successfully initialized Telegram Bot")
    except Exception as e:
        logger.error("Error initializing Telegram Bot: %s", e, exc_info=True)
        raise e

# Start the Telegram Bot in case of local debugging
def StartBot():
    bot.infinity_polling()

# Process new update from Telegram API
def ProcessUpdate(update: Update):
    bot.process_new_updates(
        updates=[update]
    )

# Handle commands sent to the bot
def HandleCommand(message: Message):
    try:
        user_id = message.from_user.id
        command = message.text
        user_info = GetUserInfoByID(user_id, message.from_user.username, message.chat.id)
        chat_id = user_info['chat_id']
        language = user_info['bot_language']
        command_disallowed = False
        
        match command.lower():
            case '/start':
                Start(bot, chat_id, language)
            case '/help':
                Help(bot, chat_id, language, user_info['user_role'])
            case '/language':
                Language(bot, chat_id, language)
            case '/budget':
                Budget(bot, chat_id, language, user_info['user_budget'])
            case '/reset':
                if user_info['user_role'] in ('owner', 'admin', 'user', ):
                    Reset(bot, chat_id, language)
                else:
                    command_disallowed = True
            case '/summarize':
                if user_info['user_role'] in ('owner', 'admin', 'user', ):
                    Summarize(bot, user_id, chat_id, language)
                else:
                    command_disallowed = True
            case '/settings':
                if user_info['user_role'] in ('owner', 'admin', ):
                    Settings(bot, chat_id, language)
                else:
                    command_disallowed = True
            case '/users':
                if user_info['user_role'] in ('owner', ):
                    Users(bot, chat_id, language)
                else:
                    command_disallowed = True
            case _:
                HandleUnknownCommand(bot, message, language)
                logger.warning(f"Unsupported command '{command}' received from user #{user_id}")
        
        if command_disallowed:
            HandleDisallowedCommand(bot, message, language)
            logger.warning(f"Disallowed command '{command}' received from user #{user_id}")

        UpdateBotCommands(bot, chat_id, user_info['user_role'], language)
        
        logger.info(f"Successfully processed bot command '{command}' for user #{user_id}")
    except Exception as e:
        logger.error(f"Error processing bot command '{command}' for user #{user_id}: {str(e)}", exc_info=True)

# Handle messages sent to the bot
def HandleMessage(message: Message):
    try:
        user_id = message.from_user.id
        message_type = message.content_type
        user_info = GetUserInfoByID(user_id, message.from_user.username, message.chat.id)
        language = user_info['bot_language']

        if user_info['user_role'] not in ('owner', 'admin', 'user', ):
            HandleDisallowedMessage(bot, message, user_info)
            logger.warning(f"User #{user_id} is not allowed to send messages to the bot")
            return

        match message_type.lower():
            case 'text':
                if message.text.startswith('/'):
                    HandleCommand(message)
                else:
                    HandleTextMessage(bot, message, user_info)
            case 'photo':
                HandlePhotoMessage(bot, message, user_info)
            case 'audio':
                HandleAudioMessage(bot, message, user_info)
            case 'voice':
                HandleVoiceMessage(bot, message, user_info)
            case 'video':
                HandleVideoMessage(bot, message, user_info)
            case 'video_note':
                HandleVideoNoteMessage(bot, message, user_info)
            case 'document':
                HandleDocumentMessage(bot, message, user_info)
            case 'dice':
                HandleDiceMessage(bot, message, user_info)
            case _:
                HandleUnknownMessage(bot, message, language)
                logger.warning(f"Message of unsupported type '{message_type}' received from user #{user_id}")
        
        UpdateBotCommands(bot, user_info['chat_id'], user_info['user_role'], language)
        
        logger.info(f"Successfully processed message of type '{message_type}' from user #{user_id}")
    except Exception as e:
        logger.error(f"Error processing message of type '{message_type}' from user #{user_id}: {str(e)}", exc_info=True)

# Handle callback queries sent to the bot
def HandleCallbackQuery(call: CallbackQuery):
    try:
        user_id = call.from_user.id
        data = call.data

        user_info = GetUserInfoByID(user_id, call.from_user.username, call.message.chat.id)
        
        call_data = data.split('_')
        if len(call_data) == 0:
            HandleUnknownCallbackQuery(bot, call.id, call_data, user_id, user_info)
        else:
            category = call_data[0]

            match category.lower():
                case 'language':
                    user_info = HandleLanguageCallbackQuery(bot, call.id, call_data, call.message.message_id, user_id, user_info)
                case 'settings':
                    user_info = HandleSettingsCallbackQuery(bot, call.id, call_data, call.message.message_id, user_id, user_info)
                case 'reset':
                    user_info = HandleResetCallbackQuery(bot, call.id, call_data, call.message.message_id, user_id, user_info)
                case 'manage':
                    user_info = HandleManagementCallbackQuery(bot, call.id, call_data, call.message.message_id, user_id, user_info)
                case _:
                    HandleUnknownCallbackQuery(bot, call.id, call_data, user_id, user_info)

        UpdateBotCommands(bot, user_info['chat_id'], user_info['user_role'], user_info['bot_language'])

        logger.info(f"Successfully processed callback query '{data}' for user #{user_id}")
    except Exception as e:
        logger.error(f"Error processing callback query '{data}' for user #{user_id}: {str(e)}", exc_info=True)