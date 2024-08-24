# Import necessary modules, classes and functions
import os
import json
from telebot.types import Update, Message, CallbackQuery
import telegram_bot
from telegram_bot import InitServiceVars, InitBot
from utils.telegram import UpdateBotCommands

# Read environment variables
env_vars = {
    'ACCESS_KEY_ID': os.environ.get('ACCESS_KEY_ID'),
    'SECRET_ACCESS_KEY': os.environ.get('SECRET_ACCESS_KEY'),
    'DOCAPI_ENDPOINT': os.environ.get('DOCAPI_ENDPOINT'),
    'TELEGRAM_BOT_TOKEN': os.environ.get('TELEGRAM_BOT_TOKEN'),
    'OWNER_TELEGRAM_ID': os.environ.get('OWNER_TELEGRAM_ID'),
    'OWNER_TELEGRAM_NAME': os.environ.get('OWNER_TELEGRAM_NAME'),
    'OPENAI_API_KEY': os.environ.get('OPENAI_API_KEY'),
    'WOLFRAM_APP_ID': os.environ.get('WOLFRAM_APP_ID'),
    'DUCKDUCKGO_SAFESEARCH': os.environ.get('DUCKDUCKGO_SAFESEARCH'),
    'WORLDTIME_DEFAULT_TIMEZONE': os.environ.get('WORLDTIME_DEFAULT_TIMEZONE'),
    'PROXY': os.environ.get('PROXY'),
}

# Initialize environment variables
InitServiceVars(env_vars)

# Initialize the Telegram Bot
bot = InitBot(env_vars)


# Handle incoming updates from Telegram
def handler(event, _):
    request_body = json.loads(event['body'])
    update = Update.de_json(request_body)
    bot.process_new_updates([update])

    return {
        'statusCode': 200
    }


# Introduce the bot to the user
@bot.message_handler(commands=["start"])
def start(message: Message):
    UpdateBotCommands(bot, message.chat.id, message.from_user.id)
    telegram_bot.Start(bot, message)

# Get the bot's help message
@bot.message_handler(commands=["help"])
def help(message: Message):
    UpdateBotCommands(bot, message.chat.id, message.from_user.id)
    telegram_bot.Help(bot, message)

# Change the bot's language for the user
@bot.message_handler(commands=["language"])
def language(message: Message):
    UpdateBotCommands(bot, message.chat.id, message.from_user.id)
    telegram_bot.Language(bot, message)

# Get the bot's budget for the user
@bot.message_handler(commands=["budget"])
def stats(message: Message):
    UpdateBotCommands(bot, message.chat.id, message.from_user.id)
    telegram_bot.Budget(bot, message)

# Reset the conversation history
@bot.message_handler(commands=["reset"])
def reset(message: Message):
    UpdateBotCommands(bot, message.chat.id, message.from_user.id)
    telegram_bot.Reset(bot, message)

# Summarize the conversation history
@bot.message_handler(commands=["summarize"])
def summarize(message: Message):
    UpdateBotCommands(bot, message.chat.id, message.from_user.id)
    telegram_bot.Summarize(bot, message)

# Get the bot's settings
@bot.message_handler(commands=["settings"])
def settings(message: Message):
    UpdateBotCommands(bot, message.chat.id, message.from_user.id)
    telegram_bot.Settings(bot, message)

# Manage users and admins of the bot
@bot.message_handler(commands=["users"])
def users(message: Message):
    UpdateBotCommands(bot, message.chat.id, message.from_user.id)
    telegram_bot.Users(bot, message)


# Handle all other messages
@bot.message_handler(func=lambda message: True, content_types=['animation', 'audio', 'contact', 'dice', 'document', 'location', 'photo', 'poll', 'sticker', 'text', 'venue', 'video', 'video_note', 'voice'])
def handle_message(message: Message):
    UpdateBotCommands(bot, message.chat.id, message.from_user.id)
    telegram_bot.HandleMessage(bot, message)


# Handle the callback query
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: CallbackQuery):
    UpdateBotCommands(bot, call.message.chat.id, call.from_user.id)
    telegram_bot.HandleCallbackQuery(bot, call)