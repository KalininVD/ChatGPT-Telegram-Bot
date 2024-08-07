# Import necessary modules, classes and functions
from decimal import Decimal
from telebot import TeleBot
from telebot.types import Message, CallbackQuery
from utils.openai import OpenAIHelper
from utils.plugins import PluginManager
from utils.telegram_inline_keyboards import (GenKBUserCategoties, GenKBAdmins, GenKBUsers, GenKBBannedUsers,
                                             GenKBAdmin, GenKBUser, GenKBBanned, GenKBLanguage, GenKBModel, GenKBBudget,
                                             GenKBDeleteAdmin, GenKBDeleteUser, GenKBDeleteBanned)
from utils.telegram import (GetCategory, GetLanguage, GetModel, GetBudget,
                            SetCategory, SetLanguage, SetModel, SetBudget,
                            DeleteUserInfo)
from utils.telegram import InitEnvVars as InitTelegramEnvVars
from utils.yandexcloud import InitEnvVars as InitYandexCloudEnvVars
from utils.openai import InitEnvVars as InitOpenAIEnvVars
from utils.plugins import InitEnvVars as InitPluginEnvVars

# Define services
openai_helper: OpenAIHelper | None = None
plugin_manager: PluginManager | None = None

# Initialize environment variables
def InitServiceVars(vars: dict):
    for InitFunc in (InitYandexCloudEnvVars, InitTelegramEnvVars, InitOpenAIEnvVars, InitPluginEnvVars):
        InitFunc(vars)
    
    global openai_helper, plugin_manager

    openai_helper = OpenAIHelper()
    plugin_manager = PluginManager()
    

# Handle incoming messages
def HandleMessage(telegram_bot: TeleBot, message: Message):
    user = message.from_user
    if GetCategory(user.id, user.username) in ('banned', 'unknown'):
        SendBannedResponse(telegram_bot, message)
        return

    match message.content_type:
        case 'text':
            HandleTextMessage(telegram_bot, message)
        case 'photo':
            HandlePhotoMessage(telegram_bot, message)
        case 'audio' | 'voice':
            HandleAudioMessage(telegram_bot, message)
        case 'video' | 'video_note':
            HandleVideoMessage(telegram_bot, message)
        case 'document':
            HandleDocumentMessage(telegram_bot, message)
        case 'dice':
            HandleDiceMessage(telegram_bot, message)
        case _:
            SendDefaultResponse(telegram_bot, message)

# Handle text messages
def HandleTextMessage(telegram_bot: TeleBot, message: Message):
    telegram_bot.send_message(message.chat.id, reply_to_message_id=message.message_id, text=message.text)

# Handle photo messages
def HandlePhotoMessage(telegram_bot: TeleBot, message: Message):
    telegram_bot.send_photo(message.chat.id, reply_to_message_id=message.message_id, photo=message.photo.file_id)

# Handle audio messages
def HandleAudioMessage(telegram_bot: TeleBot, message: Message):
    if message.voice:
        telegram_bot.send_voice(message.chat.id, reply_to_message_id=message.message_id, voice=message.voice.file_id)
    else:
        telegram_bot.send_audio(message.chat.id, reply_to_message_id=message.message_id, audio=message.audio.file_id)

# Handle video messages
def HandleVideoMessage(telegram_bot: TeleBot, message: Message):
    if message.video_note:
        telegram_bot.send_video_note(message.chat.id, reply_to_message_id=message.message_id, video_note=message.video_note.file_id)
    else:
        telegram_bot.send_video(message.chat.id, reply_to_message_id=message.message_id, video=message.video.file_id)

# Handle document messages
def HandleDocumentMessage(telegram_bot: TeleBot, message: Message):
    telegram_bot.send_document(message.chat.id, reply_to_message_id=message.message_id, document=message.document.file_id)

# Handle dice messages
def HandleDiceMessage(telegram_bot: TeleBot, message: Message):
    telegram_bot.send_dice(message.chat.id, reply_to_message_id=message.message_id, emoji=message.dice.emoji)

# Send a default response to the user
def SendDefaultResponse(telegram_bot: TeleBot, message: Message):
    telegram_bot.reply_to(message, "Sorry, I can't understand this message. Please send something else to me")

# Send the response to any banned or unknown user
def SendBannedResponse(telegram_bot: TeleBot, message: Message):
    telegram_bot.send_message(message.chat.id, "Sorry, you are banned from using this bot. Please contact the bot owner for more information.")


# Send a start message to the user
def Start(telegram_bot: TeleBot, message: Message):
    telegram_bot.send_message(message.chat.id, "Hello! I'm ChatGPT Telegram Bot. I can help you with your questions and tasks. Just send me a message and I'll do my best to answer it.")

# Send a help message to the user
def Help(telegram_bot: TeleBot, message: Message):
    telegram_bot.send_message(message.chat.id, "I can help you with your questions and tasks. Just send me a message and I'll do my best to answer it.")

# Change the bot's language for the user
def ChangeLanguage(telegram_bot: TeleBot, message: Message):
    telegram_bot.send_message(message.chat.id, "# in the future you will be able to change the language of the bot #")

# Reset the conversation history
def Reset(telegram_bot: TeleBot, message: Message):
    user = message.from_user
    if GetCategory(user.id, user.username) not in ('owner', 'admin', 'user'):
        SendDisallowedResponse(telegram_bot, message)
        return
    
    telegram_bot.send_message(message.chat.id, "# in the future you will be able to reset the conversation history #")

# Summarize the conversation
def Summarize(telegram_bot: TeleBot, message: Message):
    user = message.from_user
    if GetCategory(user.id, user.username) not in ('owner', 'admin', 'user'):
        SendDisallowedResponse(telegram_bot, message)
        return
    
    telegram_bot.send_message(message.chat.id, "# in the future you will be able to summarize the conversation #")

# Get the bot's statistics
def Stats(telegram_bot: TeleBot, message: Message):
    user = message.from_user
    if GetCategory(user.id, user.username) not in ('owner', 'admin', 'user'):
        SendDisallowedResponse(telegram_bot, message)
        return
    
    telegram_bot.send_message(message.chat.id, "# in the future you will be able to get the statistics of the bot #")

# Get the bot's settings
def Settings(telegram_bot: TeleBot, message: Message):
    user = message.from_user
    if GetCategory(user.id, user.username) not in ('owner', 'admin'):
        SendDisallowedResponse(telegram_bot, message)
        return
    
    telegram_bot.send_message(message.chat.id, "# in the future you will be able to get the settings of the bot #")

# Manage users and admins of the bot
def Users(telegram_bot: TeleBot, message: Message):
    user = message.from_user
    if GetCategory(user.id, user.username) != 'owner':
        SendDisallowedResponse(telegram_bot, message)
        return
    
    telegram_bot.send_message(message.chat.id, "Let's manage the users of the bot:", reply_markup=GenKBUserCategoties())

# Send the response to any user tried to use disallowed commands
def SendDisallowedResponse(telegram_bot: TeleBot, message: Message):
    telegram_bot.send_message(message.chat.id, "Sorry, you are not allowed to use this command. Please contact the bot owner for more information.")

# Handle the callback query
def HandleCallbackQuery(telegram_bot: TeleBot, call: CallbackQuery):
    if GetCategory(call.from_user.id, call.from_user.username) != 'owner':
        telegram_bot.answer_callback_query(call.id, "Sorry, you are not allowed to use this command. Please contact the bot owner for more information.", show_alert=True)
        return

    message = call.message
    data = call.data
    chat_id = message.chat.id
    message_id = message.message_id

    if data.startswith('manage_'):
        data = data[7:]

        if data == 'bot':
            telegram_bot.edit_message_text("Let's manage the users of the Bot:",
                                           chat_id, message_id, reply_markup=GenKBUserCategoties())
        elif data == 'admins':
            telegram_bot.edit_message_text("Managing admins of the Bot:",
                                           chat_id, message_id, reply_markup=GenKBAdmins())
        elif data == 'users':
            telegram_bot.edit_message_text("Managing users of the Bot:",
                                           chat_id, message_id, reply_markup=GenKBUsers())
        elif data == 'banned':
            telegram_bot.edit_message_text("Managing banned users of the Bot:",
                                           chat_id, message_id, reply_markup=GenKBBannedUsers())
        elif data.startswith('admin_'):
            user_id = int(data[6:])
            user_name = telegram_bot.get_chat_member(chat_id, user_id).user.username
            telegram_bot.edit_message_text(f"What do you want to do for the admin {user_name}?",
                                           chat_id, message_id, reply_markup=GenKBAdmin(user_id))
        elif data.startswith('user_'):
            user_id = int(data[5:])
            user_name = telegram_bot.get_chat_member(chat_id, user_id).user.username
            telegram_bot.edit_message_text(f"What do you want to do for the user {user_name}?",
                                           chat_id, message_id, reply_markup=GenKBUser(user_id))
        elif data.startswith('banned_'):
            user_id = int(data[7:])
            user_name = telegram_bot.get_chat_member(chat_id, user_id).user.username
            telegram_bot.edit_message_text(f"What do you want to do with the banned user {user_name}?",
                                           chat_id, message_id, reply_markup=GenKBBanned(user_id))
        elif data.startswith('language_'):
            user_id = int(data[9:])
            user_name = telegram_bot.get_chat_member(chat_id, user_id).user.username
            telegram_bot.edit_message_text(f"Which language do you want to choose for the user {user_name}?\n" +
                                           f"(Current language: {GetLanguage(user_id, user_name)})",
                                           chat_id, message_id, reply_markup=GenKBLanguage(user_id))
        elif data.startswith('model_'):
            user_id = int(data[6:])
            user_name = telegram_bot.get_chat_member(chat_id, user_id).user.username
            telegram_bot.edit_message_text(f"Which model do you want to choose for the user {user_name}?\n" +
                                           f"(Current model: {GetModel(user_id, user_name)})",
                                           chat_id, message_id, reply_markup=GenKBModel(user_id))
        elif data.startswith('budget_'):
            user_id = int(data[7:])
            user_name = telegram_bot.get_chat_member(chat_id, user_id).user.username
            telegram_bot.edit_message_text(f"What do you want to do with the budget of the user {user_name}?\n" +
                                           f"(Current budget: {GetBudget(user_id, user_name)})",
                                           chat_id, message_id, reply_markup=GenKBBudget(user_id))
        else:
            telegram_bot.answer_callback_query(call.id, "Something went wrong inside the bot. Try to repeat the command later or contact the bot owner for more information.", show_alert=True)

    elif data.startswith('change_'):
        data = data[7:]

        if data.startswith('role_'):
            data = data[5:]

            if data.startswith('admin_'):
                user_id = int(data[6:])
                user_name = telegram_bot.get_chat_member(chat_id, user_id).user.username
                SetCategory(user_id, user_name, 'admin')
                telegram_bot.answer_callback_query(call.id, f"User {user_name} is now an Admin of the Bot", show_alert=True)
                telegram_bot.edit_message_text("Let's manage the users of the Bot:",
                                               chat_id, message_id, reply_markup=GenKBUserCategoties())
            elif data.startswith('user_'):
                user_id = int(data[5:])
                user_name = telegram_bot.get_chat_member(chat_id, user_id).user.username
                SetCategory(user_id, user_name, 'user')
                telegram_bot.answer_callback_query(call.id, f"User {user_name} is now a User of the Bot", show_alert=True)
                telegram_bot.edit_message_text("Let's manage the users of the Bot:",
                                               chat_id, message_id, reply_markup=GenKBUserCategoties())
            elif data.startswith('banned_'):
                user_id = int(data[7:])
                user_name = telegram_bot.get_chat_member(chat_id, user_id).user.username
                SetCategory(user_id, user_name, 'banned')
                telegram_bot.answer_callback_query(call.id, f"User {user_name} is now a Banned User of the Bot", show_alert=True)
                telegram_bot.edit_message_text("Let's manage the users of the Bot:",
                                               chat_id, message_id, reply_markup=GenKBUserCategoties())
            else:
                telegram_bot.answer_callback_query(call.id, "Something went wrong inside the bot. Try to repeat the command later or contact the bot owner for more information.", show_alert=True)

        elif data.startswith('language_'):
            data = data[9:]

            if data.startswith('en_'):
                user_id = int(data[3:])
                user_name = telegram_bot.get_chat_member(chat_id, user_id).user.username
                SetLanguage(user_id, user_name, 'en')
                telegram_bot.answer_callback_query(call.id, f"Bot language for the user {user_name} was set to English")
                telegram_bot.edit_message_text(f"What do you want to do for the user {user_name}?",
                                               chat_id, message_id, reply_markup=GenKBUser(user_id))
            elif data.startswith('ru_'):
                user_id = int(data[3:])
                user_name = telegram_bot.get_chat_member(chat_id, user_id).user.username
                SetLanguage(user_id, user_name, 'ru')
                telegram_bot.answer_callback_query(call.id, f"Bot language for the user {user_name} was set to Russian")
                telegram_bot.edit_message_text(f"What do you want to do for the user {user_name}?",
                                               chat_id, message_id, reply_markup=GenKBUser(user_id))
            else:
                telegram_bot.answer_callback_query(call.id, "Something went wrong inside the bot. Try to repeat the command later or contact the bot owner for more information.", show_alert=True)

        elif data.startswith('model_'):
            data = data[6:]

            if data.startswith('gpt35_'):
                user_id = int(data[6:])
                user_name = telegram_bot.get_chat_member(chat_id, user_id).user.username
                SetModel(user_id, user_name, 'gpt-3.5-turbo')
                telegram_bot.answer_callback_query(call.id, f"Bot model for the user {user_name} was set to gpt-3.5-turbo")
                telegram_bot.edit_message_text(f"What do you want to do for the user {user_name}?",
                                               chat_id, message_id, reply_markup=GenKBUser(user_id))
            elif data.startswith('gpt4_'):
                user_id = int(data[6:])
                user_name = telegram_bot.get_chat_member(chat_id, user_id).user.username
                SetModel(user_id, user_name, 'gpt-4')
                telegram_bot.answer_callback_query(call.id, f"Bot model for the user {user_name} was set to gpt-4")
                telegram_bot.edit_message_text(f"What do you want to do for the user {user_name}?",
                                               chat_id, message_id, reply_markup=GenKBUser(user_id))
            else:
                telegram_bot.answer_callback_query(call.id, "Something went wrong inside the bot. Try to repeat the command later or contact the bot owner for more information.", show_alert=True)

        elif data.startswith('budget_'):
            data = data[7:]

            if data.startswith('plus_'):
                user_id = int(data[5:])
                user_name = telegram_bot.get_chat_member(chat_id, user_id).user.username
                SetBudget(user_id, user_name, Decimal(GetBudget(user_id, user_name)) + Decimal(0.1))
                telegram_bot.answer_callback_query(call.id, f"Bot budget for the user {user_name} was increased by 0.1 and is now {GetBudget(user_id, user_name)}")
                telegram_bot.edit_message_text(f"What do you want to do for the user {user_name}?",
                                               chat_id, message_id, reply_markup=GenKBUser(user_id))
            elif data.startswith('minus_'):
                user_id = int(data[6:])
                user_name = telegram_bot.get_chat_member(chat_id, user_id).user.username
                if GetBudget(user_id, user_name) > Decimal(0.1):
                    SetBudget(user_id, user_name, Decimal(GetBudget(user_id, user_name)) - Decimal(0.1))
                    telegram_bot.answer_callback_query(call.id, f"Bot budget for the user {user_name} was decreased by 0.1 and is now {GetBudget(user_id, user_name)}")
                    telegram_bot.edit_message_text(f"What do you want to do for the user {user_name}?",
                                                   chat_id, message_id, reply_markup=GenKBUser(user_id))
                else:
                    SetBudget(user_id, user_name, Decimal(0))
                    telegram_bot.answer_callback_query(call.id, f"Bot budget for the user {user_name} was set to 0")
                    telegram_bot.edit_message_text(f"What do you want to do for the user {user_name}?",
                                                   chat_id, message_id, reply_markup=GenKBUser(user_id))
            else:
                telegram_bot.answer_callback_query(call.id, "Something went wrong inside the bot. Try to repeat the command later or contact the bot owner for more information.", show_alert=True)

        else:
            telegram_bot.answer_callback_query(call.id, "Something went wrong inside the bot. Try to repeat the command later or contact the bot owner for more information.", show_alert=True)
    
    elif data.startswith('delete_'):
        data = data[7:]

        if data.startswith('admin_'):
            user_id = int(data[6:])
            user_name = telegram_bot.get_chat_member(chat_id, user_id).user.username
            telegram_bot.edit_message_text(f"Do you want to delete the user {user_name} from the database of the Bot?",
                                           chat_id, message_id, reply_markup=GenKBDeleteAdmin(user_id))
        elif data.startswith('user_'):
            user_id = int(data[5:])
            user_name = telegram_bot.get_chat_member(chat_id, user_id).user.username
            telegram_bot.edit_message_text(f"Do you want to delete the user {user_name} from the database of the Bot?",
                                           chat_id, message_id, reply_markup=GenKBDeleteUser(user_id))
        elif data.startswith('banned_'):
            user_id = int(data[7:])
            user_name = telegram_bot.get_chat_member(chat_id, user_id).user.username
            telegram_bot.edit_message_text(f"Do you want to delete the user {user_name} from the database of the Bot?",
                                           chat_id, message_id, reply_markup=GenKBDeleteBanned(user_id))
        elif data.startswith('confirmed_'):
            user_id = int(data[9:])
            user_name = telegram_bot.get_chat_member(chat_id, user_id).user.username
            DeleteUserInfo(user_id, user_name)
            telegram_bot.answer_callback_query(call.id, f"User {user_name} was totally deleted from the database of the Bot", show_alert=True)
            telegram_bot.edit_message_text("Let's manage the users of the Bot:",
                                           chat_id, message_id, reply_markup=GenKBUserCategoties())
        else:
            telegram_bot.answer_callback_query(call.id, "Something went wrong inside the bot. Try to repeat the command later or contact the bot owner for more information.", show_alert=True)

    else:
        telegram_bot.answer_callback_query(call.id, "Something went wrong inside the bot. Try to repeat the command later or contact the bot owner for more information.", show_alert=True)