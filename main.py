# Import necessary modules, classes and functions
import os
import json
import logging  # Import logging for setting up logger
from telebot.types import Update, Message, CallbackQuery
import telegram_bot
from telegram_bot import InitServiceVars, InitBot
from utils.telegram import UpdateBotCommands
import telebot  # Import telebot for logging

# Set up logging
telebot.logger.setLevel(logging.INFO)  # Set the logging level to INFO
log_format = "%(asctime)s - %(levelname)s - %(message)s"  # Define log format
formatter = logging.Formatter(log_format)  # Create a formatter

# Apply the formatter to the existing handler
for handler in telebot.logger.handlers:
    handler.setFormatter(formatter)

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

# Additional logging for bot start
telebot.logger.info("Bot initialized successfully.")

# Handle incoming updates from Telegram
def handler(event, _):
    try:
        request_body = json.loads(event['body'])
        update = Update.de_json(request_body)
        bot.process_new_updates([update])
        telebot.logger.info("Processed new update successfully.")
    except Exception as e:
        telebot.logger.error("Error processing update: %s", e, exc_info=True)

    return {
        'statusCode': 200
    }

# Introduce the bot to the user
@bot.message_handler(commands=["start"])
def start(message: Message):
    try:
        UpdateBotCommands(bot, message.chat.id, message.from_user.id)
        telegram_bot.Start(bot, message)
        telebot.logger.info("Start command processed for user: %s", message.from_user.id)
        # Log successful processing
        telebot.logger.info("Successfully processed /start command for user: %s", message.from_user.id)
    except Exception as e:
        telebot.logger.error("Error processing start command: %s", e, exc_info=True)

# Get the bot's help message
@bot.message_handler(commands=["help"])
def help(message: Message):
    try:
        UpdateBotCommands(bot, message.chat.id, message.from_user.id)
        telegram_bot.Help(bot, message)
        telebot.logger.info("Help command processed for user: %s", message.from_user.id)
        # Log successful processing
        telebot.logger.info("Successfully processed /help command for user: %s", message.from_user.id)
    except Exception as e:
        telebot.logger.error("Error processing help command: %s", e, exc_info=True)

# Change the bot's language for the user
@bot.message_handler(commands=["language"])
def language(message: Message):
    try:
        UpdateBotCommands(bot, message.chat.id, message.from_user.id)
        telegram_bot.Language(bot, message)
        telebot.logger.info("Language command processed for user: %s", message.from_user.id)
        # Log successful processing
        telebot.logger.info("Successfully processed /language command for user: %s", message.from_user.id)
    except Exception as e:
        telebot.logger.error("Error processing language command: %s", e, exc_info=True)

# Get the bot's budget for the user
@bot.message_handler(commands=["budget"])
def budget(message: Message):
    try:
        UpdateBotCommands(bot, message.chat.id, message.from_user.id)
        telegram_bot.Budget(bot, message)
        telebot.logger.info("Budget command processed for user: %s", message.from_user.id)
        # Log successful processing
        telebot.logger.info("Successfully processed /budget command for user: %s", message.from_user.id)
    except Exception as e:
        telebot.logger.error("Error processing budget command: %s", e, exc_info=True)

# Reset the conversation history
@bot.message_handler(commands=["reset"])
def reset(message: Message):
    try:
        UpdateBotCommands(bot, message.chat.id, message.from_user.id)
        telegram_bot.Reset(bot, message)
        telebot.logger.info("Reset command processed for user: %s", message.from_user.id)
        # Log successful processing
        telebot.logger.info("Successfully processed /reset command for user: %s", message.from_user.id)
    except Exception as e:
        telebot.logger.error("Error processing reset command: %s", e, exc_info=True)

# Summarize the conversation history
@bot.message_handler(commands=["summarize"])
def summarize(message: Message):
    try:
        UpdateBotCommands(bot, message.chat.id, message.from_user.id)
        telegram_bot.Summarize(bot, message)
        telebot.logger.info("Summarize command processed for user: %s", message.from_user.id)
        # Log successful processing
        telebot.logger.info("Successfully processed /summarize command for user: %s", message.from_user.id)
    except Exception as e:
        telebot.logger.error("Error processing summarize command: %s", e, exc_info=True)

# Get the bot's settings
@bot.message_handler(commands=["settings"])
def settings(message: Message):
    try:
        UpdateBotCommands(bot, message.chat.id, message.from_user.id)
        telegram_bot.Settings(bot, message)
        telebot.logger.info("Settings command processed for user: %s", message.from_user.id)
        # Log successful processing
        telebot.logger.info("Successfully processed /settings command for user: %s", message.from_user.id)
    except Exception as e:
        telebot.logger.error("Error processing settings command: %s", e, exc_info=True)

# Manage users and admins of the bot
@bot.message_handler(commands=["users"])
def users(message: Message):
    try:
        UpdateBotCommands(bot, message.chat.id, message.from_user.id)
        telegram_bot.Users(bot, message)
        telebot.logger.info("Users command processed for user: %s", message.from_user.id)
        # Log successful processing
        telebot.logger.info("Successfully processed /users command for user: %s", message.from_user.id)
    except Exception as e:
        telebot.logger.error("Error processing users command: %s", e, exc_info=True)

# Handle all other messages
@bot.message_handler(func=lambda message: True, content_types=['animation', 'audio', 'contact', 'dice', 'document', 'location', 'photo', 'poll', 'sticker', 'text', 'venue', 'video', 'video_note', 'voice'])
def handle_message(message: Message):
    try:
        UpdateBotCommands(bot, message.chat.id, message.from_user.id)
        telegram_bot.HandleMessage(bot, message)
        telebot.logger.info("Handled message from user: %s", message.from_user.id)
    except Exception as e:
        telebot.logger.error("Error handling message: %s", e, exc_info=True)

# Handle the callback query
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: CallbackQuery):
    try:
        UpdateBotCommands(bot, call.message.chat.id, call.from_user.id)
        telegram_bot.HandleCallbackQuery(bot, call)
        UpdateBotCommands(bot, call.message.chat.id, call.from_user.id)
        telebot.logger.info("Callback query processed for user: %s", call.from_user.id)
    except Exception as e:
        telebot.logger.error("Error processing callback query: %s", e, exc_info=True)