# Import necessary modules, classes and functions
from decimal import Decimal
from telebot import TeleBot
from telebot.types import Message, CallbackQuery
from utils.openai import OpenAIHelper
from utils.plugins import PluginManager
import utils.inline_keyboards as kb_gen
from utils.telegram import (
    GetName, GetCategory, GetLanguage, GetModel, GetBudget,
    SetName, SetCategory, SetLanguage, SetModel, SetBudget,
    DeleteUserInfo
)
from utils.telegram import BASE_COMMANDS
from utils.telegram import InitEnvVars as InitTelegramEnvVars
from utils.yandexcloud import InitEnvVars as InitYandexCloudEnvVars
from utils.openai import InitEnvVars as InitOpenAIEnvVars
from utils.plugins import InitEnvVars as InitPluginEnvVars

# Define services
openai_helper: OpenAIHelper | None = None
plugin_manager: PluginManager | None = None

# Initialize all environment variables
def InitServiceVars(vars: dict):
    for InitFunc in (InitYandexCloudEnvVars, InitTelegramEnvVars, InitOpenAIEnvVars, InitPluginEnvVars):
        InitFunc(vars)
    
    global openai_helper, plugin_manager

    openai_helper = OpenAIHelper()
    plugin_manager = PluginManager()

# Initialize the bot
def InitBot(vars: dict) -> TeleBot:
    if any(var not in vars for var in ('TELEGRAM_BOT_TOKEN', 'OWNER_TELEGRAM_ID', 'OWNER_TELEGRAM_NAME')):
        raise ValueError("Missing environment variables. Check them all and try again.")

    bot = TeleBot(vars['TELEGRAM_BOT_TOKEN'])
    bot.set_my_commands(commands=BASE_COMMANDS)
    
    SetCategory(vars['OWNER_TELEGRAM_ID'], 'owner')
    SetName(vars['OWNER_TELEGRAM_ID'], vars['OWNER_TELEGRAM_NAME'])

    return bot

# Handle incoming messages
def HandleMessage(bot: TeleBot, message: Message):
    if GetCategory(message.from_user.id) in ('banned', 'unknown'):
        SendBannedResponse(bot, message)
        return

    match message.content_type:
        case 'text':
            HandleTextMessage(bot, message)
        case 'photo':
            HandlePhotoMessage(bot, message)
        case 'audio':
            HandleAudioMessage(bot, message)
        case 'voice':
            HandleVoiceMessage(bot, message)
        case 'video':
            HandleVideoMessage(bot, message)
        case 'video_note':
            HandleVideoNoteMessage(bot, message)
        case 'document':
            HandleDocumentMessage(bot, message)
        case 'dice':
            HandleDiceMessage(bot, message)
        case _:
            bot.reply_to(message, "Sorry, I can't understand this message. Please send something else to me")

# Handle text messages
def HandleTextMessage(bot: TeleBot, message: Message):
    bot.send_message(message.chat.id, reply_to_message_id=message.message_id, text=message.text)

# Handle photo messages
def HandlePhotoMessage(bot: TeleBot, message: Message):
    bot.send_photo(message.chat.id, reply_to_message_id=message.message_id, photo=message.photo[0].file_id)

# Handle audio messages
def HandleAudioMessage(bot: TeleBot, message: Message):
    bot.send_audio(message.chat.id, reply_to_message_id=message.message_id, audio=message.audio.file_id)

# Handle voice messages
def HandleVoiceMessage(bot: TeleBot, message: Message):
    bot.send_voice(message.chat.id, reply_to_message_id=message.message_id, voice=message.voice.file_id)

# Handle video messages
def HandleVideoMessage(bot: TeleBot, message: Message):
    bot.send_video(message.chat.id, reply_to_message_id=message.message_id, video=message.video.file_id)

# Handle video note messages
def HandleVideoNoteMessage(bot: TeleBot, message: Message):
    bot.send_video_note(message.chat.id, reply_to_message_id=message.message_id, video_note=message.video_note.file_id)

# Handle document messages
def HandleDocumentMessage(bot: TeleBot, message: Message):
    bot.send_document(message.chat.id, reply_to_message_id=message.message_id, document=message.document.file_id)

# Handle dice messages
def HandleDiceMessage(bot: TeleBot, message: Message):
    bot.send_dice(message.chat.id, reply_to_message_id=message.message_id, emoji=message.dice.emoji)

# Send the response to any banned or unknown user
def SendBannedResponse(bot: TeleBot, message: Message):
    bot.send_message(message.chat.id, "Sorry, you are banned from using this bot. Please contact the bot owner for more information.")


# Send a start message to the user
def Start(bot: TeleBot, message: Message):
    bot.send_message(message.chat.id, "Hello! I'm ChatGPT Telegram Bot. I can help you with your questions and tasks.\n"
                     "Just send me a message and I'll do my best to answer it.\n"
                     "To get started, you can use the /help command to see what I can do.")

# Send a help message to the user
def Help(bot: TeleBot, message: Message):
    help_message = "I'm ChatGPT Telegram Bot. I can help you with your questions and tasks.\n\n"
    help_message += "Here is the list of available commands:\n\n"

    help_message += "/start - Show the start message\n"
    help_message += "/help - Show this help message\n"
    help_message += "/language - Change the bot's language\n"
    help_message += "/budget - Get the bot's remeining budget\n"

    if GetCategory(message.from_user.id) in ('owner', 'admin', 'user'):
        help_message += "/reset - Reset the conversation history\n"
        help_message += "/summarize - Summarize the conversation history\n"
    
    if GetCategory(message.from_user.id) in ('owner', 'admin'):
        help_message += "/settings - Change the bot's settings\n"
    
    if GetCategory(message.from_user.id) in ('owner'):
        help_message += "/users - Manage the users of the bot\n"

    help_message += "\n\nYou can also send me any text, photo, audio and video messages and I'll do my best to handle them.\n"
    help_message += "For example, I can generate a caption for a photo or transcribe a voice message to text.\n"
    help_message += "In case of any questions or issues, please contact the bot owner."

    bot.send_message(message.chat.id, help_message)

# Change the bot's language for the user
def Language(bot: TeleBot, message: Message):
    bot.send_message(message.chat.id, "Which language do you want to choose for the bot?", reply_markup=kb_gen.LanguageGeneral())

# Get the bot's budget for the user
def Budget(bot: TeleBot, message: Message):
    bot.send_message(message.chat.id, f"Your current budget for the bot is {GetBudget(message.from_user.id)}$")

# Reset the conversation history
def Reset(bot: TeleBot, message: Message):
    if GetCategory(message.from_user.id) not in ('owner', 'admin', 'user'):
        bot.send_message(message.chat.id, "Sorry, you are not allowed to use this command. Please contact the bot owner for more information.")
        return
    
    bot.send_message(message.chat.id, "Conversation history was reset")

# Summarize the conversation
def Summarize(bot: TeleBot, message: Message):
    if GetCategory(message.from_user.id) not in ('owner', 'admin', 'user'):
        bot.send_message(message.chat.id, "Sorry, you are not allowed to use this command. Please contact the bot owner for more information.")
        return
    
    bot.send_message(message.chat.id, "# in the future you will be able to summarize the conversation #")

# Get the bot's settings
def Settings(bot: TeleBot, message: Message):
    if GetCategory(message.from_user.id) not in ('owner', 'admin'):
        bot.send_message(message.chat.id, "Sorry, you are not allowed to use this command. Please contact the bot owner for more information.")
        return
    
    bot.send_message(message.chat.id, "Which settings do you want to change for the bot?", reply_markup=kb_gen.Settings())

# Manage users and admins of the bot
def Users(bot: TeleBot, message: Message):
    if GetCategory(message.from_user.id) != 'owner':
        bot.send_message(message.chat.id, "Sorry, you are not allowed to use this command. Please contact the bot owner for more information.")
        return
    
    bot.send_message(message.chat.id, "Let's manage the users of the bot:", reply_markup=kb_gen.UserCategoties())


# Handle the callback query
def HandleCallbackQuery(bot: TeleBot, call: CallbackQuery):
    data = call.data
    user_id = call.from_user.id

    inform, edit = None, False
    answer, text = '', ''
    keyboard = None

    if data == 'language':
        edit = True
        text = "Which language do you want to choose for the bot?"
        keyboard = kb_gen.LanguageGeneral()
    elif data.startswith('language_'):
        inform = False
        if data == 'language_ru':
            SetLanguage(user_id, 'ru')
            answer = "Bot language was set to Russian"
        else:
            SetLanguage(user_id, 'en')
            answer = "Bot language was set to English"

    elif GetCategory(user_id) in ('unknown', 'banned', 'user'):
        inform = True
        answer = "Sorry, you are not allowed to use this command. Please contact the bot owner for more information."
    
    elif data == 'settings':
        edit = True
        text = "Which settings do you want to change for the bot?"
        keyboard = kb_gen.Settings()
    elif data.startswith('settings_'):
        if data == 'settings_language':
            edit = True
            text = "Which language do you want to choose for the bot?"
            keyboard = kb_gen.LanguageSettings()
        elif data.startswith('settings_language_'):
            inform = False
            if data == 'settings_language_ru':
                SetLanguage(user_id, 'ru')
                answer = "Bot language was set to Russian"
            else:
                SetLanguage(user_id, 'en')
                answer = "Bot language was set to English"

        elif data == 'settings_model':
            edit = True
            text = "Which chat model do you want to choose for the bot?"
            keyboard = kb_gen.ModelSettings()
        elif data.startswith('settings_model_'):
            inform = False
            if data == 'settings_model_gpt-4o':
                SetModel(user_id, 'gpt-4o')
                answer = "Chat model for the bot was set to gpt-4o"
            else:
                SetModel(user_id, 'gpt-4o-mini')
                answer = "Chat model for the bot was set to gpt-4o-mini"

        else:
            inform = True
            answer = "Sorry, something went wrong. Please try again later or contact the bot owner for more information."
    
    elif GetCategory(user_id) == 'admin':
        inform = True
        answer = "Sorry, you are not allowed to use this command. Please contact the bot owner for more information."

    elif data == 'manage':
        edit = True
        text = "Let's manage the users of the Bot:"
        keyboard = kb_gen.UserCategoties()
    elif data.startswith('manage_'):
        edit = True
        if data == 'manage_admins':
            text = "Managing admins of the Bot:"
            keyboard = kb_gen.Admins()
        elif data == 'manage_users':
            text = "Managing users of the Bot:"
            keyboard = kb_gen.Users()
        elif data == 'manage_banned':
            text = "Managing banned users of the Bot:"
            keyboard = kb_gen.BannedUsers()
        else:
            try:
                user_id = int(data.split('_')[-1])
                user_name = GetName(user_id)
                data = '_'.join(data.split('_')[:-1])
            except ValueError:
                data = 'error'
            
            if data == 'manage_admin':
                text = f"What do you want to do for the admin @{user_name}?"
                keyboard = kb_gen.Admin(user_id)
            elif data == 'manage_user':
                text = f"What do you want to do for the user @{user_name}?"
                keyboard = kb_gen.User(user_id)
            elif data == 'manage_banned':
                text = f"What do you want to do with the banned user @{user_name}?"
                keyboard = kb_gen.Banned(user_id)
            
            elif data.startswith('manage_role_'):
                inform = True
                text = "Let's manage the users of the Bot:"
                keyboard = kb_gen.UserCategoties()

                if data == 'manage_role_admin':
                    SetCategory(user_id, 'admin')
                    answer = f"User @{GetName(user_id)} is now an Admin of the Bot"
                elif data == 'manage_role_user':
                    SetCategory(user_id, 'user')
                    answer = f"User @{GetName(user_id)} is now a User of the Bot"
                else:
                    SetCategory(user_id, 'banned')
                    answer = f"User @{GetName(user_id)} is now a Banned User of the Bot"
            
            elif data == 'manage_language':
                edit = True
                text = f"Which language do you want to choose for the user @{user_name}?\n(Current language: {GetLanguage(user_id)})"
                keyboard = kb_gen.Language(user_id)
            elif data.startswith('manage_language_'):
                inform = False
                if data == 'manage_language_ru':
                    SetLanguage(user_id, 'ru')
                    answer = f"Bot language for the user @{user_name} was set to Russian"
                else:
                    SetLanguage(user_id, 'en')
                    answer = f"Bot language for the user @{user_name} was set to English"

            elif data == 'manage_model':
                edit = True
                text = f"Which model do you want to choose for the user @{user_name}?\n(Current model: {GetModel(user_id)})"
                keyboard = kb_gen.Model(user_id)
            elif data.startswith('manage_model_'):
                inform = False
                if data == 'manage_model_gpt4o':
                    SetModel(user_id, 'gpt-4o')
                    answer = f"Bot model for the user @{user_name} was set to gpt-4o"
                else:
                    SetModel(user_id, 'gpt-4o-mini')
                    answer = f"Bot model for the user @{user_name} was set to gpt-4o-mini"

            elif data == 'manage_budget':
                edit = True
                text = f"What do you want to do with the budget of the user @{user_name}?\n(Current budget: {GetBudget(user_id)})"
                keyboard = kb_gen.Budget(user_id)
            elif data.startswith('manage_budget_'):
                inform = False
                if data == 'manage_budget_increase':
                    SetBudget(user_id, GetBudget(user_id) + Decimal('0.1'))
                    answer = f"Bot budget for the user @{user_name} was increased by 0.1$ and is now {GetBudget(user_id)}$"
                else:
                    if GetBudget(user_id) > Decimal(0.1):
                        SetBudget(user_id, GetBudget(user_id) - Decimal('0.1'))
                        answer = f"Bot budget for the user @{user_name} was decreased by 0.1$ and is now {GetBudget(user_id)}$"
                    else:
                        SetBudget(user_id, Decimal(0))
                        answer = f"Bot budget for the user @{user_name} was set to 0$"

            elif data.startswith('manage_delete_'):
                edit = True
                if data == 'manage_delete_admin':
                    text = f"Do you want to delete the user @{user_name} (is now an Admin) from the database of the Bot?"
                    keyboard = kb_gen.DeleteAdmin(user_id)
                elif data == 'manage_delete_user':
                    text = f"Do you want to delete the user @{user_name} (is now a User) from the database of the Bot?"
                    keyboard = kb_gen.DeleteUser(user_id)
                else:
                    text = f"Do you want to delete the user @{user_name} (is now a Banned User) from the database of the Bot?"
                    keyboard = kb_gen.DeleteBanned(user_id)

            elif data.startswith('manage_remove_'):
                DeleteUserInfo(user_id)
                inform = True
                answer = f"User @{GetName(user_id)} was totally deleted from the database of the Bot"
                edit = True
                if data == 'manage_remove_admin':
                    text = "Managing admins of the Bot:"
                    keyboard = kb_gen.Admins()
                elif data == 'manage_remove_user':
                    text = "Managing users of the Bot:"
                    keyboard = kb_gen.Users()
                else:
                    text = "Managing banned users of the Bot:"
                    keyboard = kb_gen.BannedUsers()

            else:
                inform = True
                answer = "Sorry, something went wrong. Please try again later or contact the bot owner for more information."
    else:
        inform = True
        answer = "Sorry, something went wrong. Please try again later or contact the bot owner for more information."

    if inform is not None:
        bot.answer_callback_query(call.id, answer, show_alert=inform)
    if edit:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=keyboard)