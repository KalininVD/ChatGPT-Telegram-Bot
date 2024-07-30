# Import the necessary modules
import os
import json
from telebot import TeleBot
from telebot.types import Update, Message
import bot
from openai_helper import OpenAIHelper
from plugin_manager import PluginManager
import utils
from utils import BASE_COMMANDS, UpdateBotCommands, SetUserCategory

# Get the environment variables
utils.SECRET_ID = os.environ.get('SECRET_ID')
utils.DOCAPI_ENDPOINT = os.environ.get('DOCAPI_ENDPOINT')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
OWNER_TELEGRAM_ID = os.environ.get('OWNER_TELEGRAM_ID')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
WOLFRAM_APP_ID = os.environ.get('WOLFRAM_APP_ID')
DUCKDUCKGO_SAFESEARCH = os.environ.get('DUCKDUCKGO_SAFESEARCH')
WORLDTIME_DEFAULT_TIMEZONE = os.environ.get('WORLDTIME_DEFAULT_TIMEZONE')

# Initialize the Telegram Bot
telegram_bot = TeleBot(TELEGRAM_BOT_TOKEN, threaded=False)
telegram_bot.set_my_commands(commands=BASE_COMMANDS)
SetUserCategory(OWNER_TELEGRAM_ID, 'owner')
openai_helper = OpenAIHelper(OPENAI_API_KEY)
plugin_manager = PluginManager(WOLFRAM_APP_ID, DUCKDUCKGO_SAFESEARCH, WORLDTIME_DEFAULT_TIMEZONE)

# Handle incoming updates from Telegram
def handler(event, _):
    request_body = json.loads(event['body'])
    update = Update.de_json(request_body)
    telegram_bot.process_new_updates([update])

    return {
        'statusCode': 200
    }


# Introduce the bot to the user
@telegram_bot.message_handler(commands=["start"])
def start(message: Message):
    UpdateBotCommands(telegram_bot, message.chat.id, message.from_user.id)
    bot.Start(telegram_bot, message)

# Get the bot's help message
@telegram_bot.message_handler(commands=["help"])
def help(message: Message):
    UpdateBotCommands(telegram_bot, message.chat.id, message.from_user.id)
    bot.Help(telegram_bot, message)

# Change the bot's language for the user
@telegram_bot.message_handler(commands=["change_language"])
def change_language(message: Message):
    UpdateBotCommands(telegram_bot, message.chat.id, message.from_user.id)
    bot.ChangeLanguage(telegram_bot, openai_helper, message)

# Change the bot's model for the user
@telegram_bot.message_handler(commands=["change_model"])
def change_model(message: Message):
    UpdateBotCommands(telegram_bot, message.chat.id, message.from_user.id)
    bot.ChangeModel(telegram_bot, openai_helper, message)

# Manage users and admins of the bot
@telegram_bot.message_handler(commands=["users"])
def users(message: Message):
    UpdateBotCommands(telegram_bot, message.chat.id, message.from_user.id)
    bot.Users(telegram_bot, message)

# Get the bot's statistics
@telegram_bot.message_handler(commands=["stats"])
def stats(message: Message):
    UpdateBotCommands(telegram_bot, message.chat.id, message.from_user.id)
    bot.Stats(telegram_bot, openai_helper, message)

# Get the bot's settings
@telegram_bot.message_handler(commands=["settings"])
def settings(message: Message):
    UpdateBotCommands(telegram_bot, message.chat.id, message.from_user.id)
    bot.Settings(telegram_bot, openai_helper, message)

# Reset the conversation history
@telegram_bot.message_handler(commands=["reset"])
def reset(message: Message):
    UpdateBotCommands(telegram_bot, message.chat.id, message.from_user.id)
    bot.Reset(telegram_bot, openai_helper, message)

# Summarize the conversation history
@telegram_bot.message_handler(commands=["summarize"])
def summarize(message: Message):
    UpdateBotCommands(telegram_bot, message.chat.id, message.from_user.id)
    bot.Summarize(telegram_bot, openai_helper, message)


# Handle all other messages
@telegram_bot.message_handler(func=lambda message: True, content_types=['animation', 'audio', 'contact', 'dice', 'document', 'location', 'photo', 'poll', 'sticker', 'text', 'venue', 'video', 'video_note', 'voice'])
def handle_message(message: Message):
    UpdateBotCommands(telegram_bot, message.chat.id, message.from_user.id)
    bot.HandleMessage(telegram_bot, openai_helper, plugin_manager, message)