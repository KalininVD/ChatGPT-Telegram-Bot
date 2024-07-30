# Import the necessary modules
from telebot import TeleBot
from telebot.types import Message
from openai_helper import OpenAIHelper
from plugin_manager import PluginManager
from utils import GetUserCategory

# Handle incoming messages
def HandleMessage(telegram_bot: TeleBot, openai_helper: OpenAIHelper, plugin_manager: PluginManager, message: Message):
    if GetUserCategory(message.from_user.id) in ('banned', 'unknown'):
        SendBannedResponse(telegram_bot, message)
        return

    match message.content_type:
        case 'text':
            HandleTextMessage(telegram_bot, openai_helper, plugin_manager, message)
        case 'photo':
            HandlePhotoMessage(telegram_bot, openai_helper, plugin_manager, message)
        case 'audio' | 'voice':
            HandleAudioMessage(telegram_bot, openai_helper, plugin_manager, message)
        case 'video' | 'video_note':
            HandleVideoMessage(telegram_bot, openai_helper, plugin_manager, message)
        case 'document':
            HandleDocumentMessage(telegram_bot, openai_helper, plugin_manager, message)
        case 'dice':
            HandleDiceMessage(telegram_bot, message)
        case _:
            SendDefaultResponse(telegram_bot, message)

# Handle text messages
def HandleTextMessage(telegram_bot: TeleBot, openai_helper: OpenAIHelper, plugin_manager: PluginManager, message: Message):
    text = message.text
    telegram_bot.reply_to(message, text)

# Handle photo messages
def HandlePhotoMessage(telegram_bot: TeleBot, openai_helper: OpenAIHelper, plugin_manager: PluginManager, message: Message):
    photo = message.photo
    telegram_bot.reply_to(message, photo)

# Handle audio messages
def HandleAudioMessage(telegram_bot: TeleBot, openai_helper: OpenAIHelper, plugin_manager: PluginManager, message: Message):
    audio = message.audio or message.voice
    telegram_bot.reply_to(message, audio)

# Handle video messages
def HandleVideoMessage(telegram_bot: TeleBot, openai_helper: OpenAIHelper, plugin_manager: PluginManager, message: Message):
    video = message.video or message.video_note
    telegram_bot.reply_to(message, video)

# Handle document messages
def HandleDocumentMessage(telegram_bot: TeleBot, openai_helper: OpenAIHelper, plugin_manager: PluginManager, message: Message):
    document = message.document
    telegram_bot.reply_to(message, document)

# Handle dice messages
def HandleDiceMessage(telegram_bot: TeleBot, message: Message):
    dice = message.dice
    telegram_bot.reply_to(message, dice)

# Send a default response to the user
def SendDefaultResponse(telegram_bot: TeleBot, message: Message):
    telegram_bot.reply_to(message, "Sorry, I can't understand this message. Please send something else to me")

# Send the response to any banned or unknown user
def SendBannedResponse(telegram_bot: TeleBot, message: Message):
    telegram_bot.send_message(message.chat.id, "Sorry, you are banned from using this bot. Please contact the bot owner for more information.")

# Send the response to any user tried to use disallowed commands
def SendDisallowedResponse(telegram_bot: TeleBot, message: Message):
    telegram_bot.send_message(message.chat.id, "Sorry, you are not allowed to use this command. Please contact the bot owner for more information.")

# Send a start message to the user
def Start(telegram_bot: TeleBot, message: Message):
    telegram_bot.send_message(message.chat.id, "Hello! I'm ChatGPT Telegram Bot. I can help you with your questions and tasks. Just send me a message and I'll do my best to answer it.")

# Send a help message to the user
def Help(telegram_bot: TeleBot, message: Message):
    telegram_bot.send_message(message.chat.id, "I can help you with your questions and tasks. Just send me a message and I'll do my best to answer it.")

# Change the bot's language for the user
def ChangeLanguage(telegram_bot: TeleBot, openai_helper: OpenAIHelper, message: Message):
    telegram_bot.send_message(message.chat.id, "# in the future you will be able to change the language of the bot #")

# Change the bot's model for the user
def ChangeModel(telegram_bot: TeleBot, openai_helper: OpenAIHelper, message: Message):
    if GetUserCategory(message.from_user.id) not in ('owner', 'admin'):
        SendDisallowedResponse(telegram_bot, message)
        return
    
    telegram_bot.send_message(message.chat.id, "# in the future you will be able to change the model of the bot #")

# Manage users and admins of the bot
def Users(telegram_bot: TeleBot, message: Message):
    if GetUserCategory(message.from_user.id) != 'owner':
        SendDisallowedResponse(telegram_bot, message)
        return
    
    telegram_bot.send_message(message.chat.id, "# in the future you will be able to manage the users of the bot #")

# Get the bot's statistics
def Stats(telegram_bot: TeleBot, openai_helper: OpenAIHelper, message: Message):
    if GetUserCategory(message.from_user.id) not in ('owner', 'admin', 'user'):
        SendDisallowedResponse(telegram_bot, message)
        return
    
    telegram_bot.send_message(message.chat.id, "# in the future you will be able to get the statistics of the bot #")

# Get the bot's settings
def Settings(telegram_bot: TeleBot, openai_helper: OpenAIHelper, message: Message):
    if GetUserCategory(message.from_user.id) not in ('owner', 'admin'):
        SendDisallowedResponse(telegram_bot, message)
        return
    
    telegram_bot.send_message(message.chat.id, "# in the future you will be able to get the settings of the bot #")

# Reset the conversation history
def Reset(telegram_bot: TeleBot, openai_helper: OpenAIHelper, message: Message):
    if GetUserCategory(message.from_user.id) not in ('owner', 'admin', 'user'):
        SendDisallowedResponse(telegram_bot, message)
        return
    
    telegram_bot.send_message(message.chat.id, "# in the future you will be able to reset the conversation history #")

# Summarize the conversation
def Summarize(telegram_bot: TeleBot, openai_helper: OpenAIHelper, message: Message):
    if GetUserCategory(message.from_user.id) not in ('owner', 'admin', 'user'):
        SendDisallowedResponse(telegram_bot, message)
        return
    
    telegram_bot.send_message(message.chat.id, "# in the future you will be able to summarize the conversation #")