# Import necessary modules, classes and functions
from decimal import Decimal
from telebot import TeleBot
from telebot.types import Message, CallbackQuery
from utils.openai import OpenAIHelper
from utils.plugins import PluginManager
from utils.telegram_inline_keyboards import (GenKBUserCategoties, GenKBAdmins, GenKBUsers, GenKBBannedUsers,
                                             GenKBAdmin, GenKBUser, GenKBBanned, GenKBLanguage, GenKBModel, GenKBBudget,
                                             GenKBDeleteAdmin, GenKBDeleteUser, GenKBDeleteBanned,
                                             GenKBLanguageGeneral, GenKBLanguageSettings, GenKBModelSettings, GenKBSettings)
from utils.telegram import (GetName, GetCategory, GetLanguage, GetModel, GetBudget,
                            SetName, SetCategory, SetLanguage, SetModel, SetBudget,
                            DeleteUserInfo)
from utils.telegram import BASE_COMMANDS
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

# Initialize the bot
def InitBot(vars: dict) -> TeleBot:
    telegram_bot = TeleBot(vars['TELEGRAM_BOT_TOKEN'])
    telegram_bot.set_my_commands(commands=BASE_COMMANDS)
    
    SetCategory(vars['OWNER_TELEGRAM_ID'], 'owner')
    SetName(vars['OWNER_TELEGRAM_ID'], vars['OWNER_TELEGRAM_NAME'])

    return telegram_bot

# Handle incoming messages
def HandleMessage(telegram_bot: TeleBot, message: Message):
    if GetCategory(message.from_user.id) in ('banned', 'unknown'):
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
    telegram_bot.send_photo(message.chat.id, reply_to_message_id=message.message_id, photo=message.photo[0].file_id)

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
def Language(telegram_bot: TeleBot, message: Message):
    telegram_bot.send_message(message.chat.id, "Which language do you want to choose for the bot?", reply_markup=GenKBLanguageGeneral())

# Get the bot's budget for the user
def Budget(telegram_bot: TeleBot, message: Message):
    telegram_bot.send_message(message.chat.id, f"Your current budget for the bot is {GetBudget(message.from_user.id)}$")

# Reset the conversation history
def Reset(telegram_bot: TeleBot, message: Message):
    if GetCategory(message.from_user.id) not in ('owner', 'admin', 'user'):
        SendDisallowedResponse(telegram_bot, message)
        return
    
    telegram_bot.send_message(message.chat.id, "# in the future you will be able to reset the conversation history #")

# Summarize the conversation
def Summarize(telegram_bot: TeleBot, message: Message):
    if GetCategory(message.from_user.id) not in ('owner', 'admin', 'user'):
        SendDisallowedResponse(telegram_bot, message)
        return
    
    telegram_bot.send_message(message.chat.id, "# in the future you will be able to summarize the conversation #")

# Get the bot's settings
def Settings(telegram_bot: TeleBot, message: Message):
    if GetCategory(message.from_user.id) not in ('owner', 'admin'):
        SendDisallowedResponse(telegram_bot, message)
        return
    
    telegram_bot.send_message(message.chat.id, "Which settings do you want to change for the bot?", reply_markup=GenKBSettings())

# Manage users and admins of the bot
def Users(telegram_bot: TeleBot, message: Message):
    if GetCategory(message.from_user.id) != 'owner':
        SendDisallowedResponse(telegram_bot, message)
        return
    
    telegram_bot.send_message(message.chat.id, "Let's manage the users of the bot:", reply_markup=GenKBUserCategoties())

# Send the response to any user tried to use disallowed commands
def SendDisallowedResponse(telegram_bot: TeleBot, message: Message):
    telegram_bot.send_message(message.chat.id, "Sorry, you are not allowed to use this command. Please contact the bot owner for more information.")

# Handle the callback query
def HandleCallbackQuery(telegram_bot: TeleBot, call: CallbackQuery):
    call_id = call.id
    message = call.message
    data = call.data
    chat_id = message.chat.id
    message_id = message.message_id
    user = call.from_user
    user_id = user.id

    if data.startswith('language'):
        if data == 'language_en':
            SetLanguage(user_id, 'en')
            telegram_bot.answer_callback_query(call_id, f"Bot language was set to English")
        elif data == 'language_ru':
            SetLanguage(user_id, 'ru')
            telegram_bot.answer_callback_query(call_id, f"Bot language was set to Russian")
        
        telegram_bot.edit_message_text(f"Which language do you want to choose for the bot?",
                                       chat_id, message_id, reply_markup=GenKBLanguageGeneral())

    elif data.startswith('settings'):
        if GetCategory(user_id) not in ('owner', 'admin'):
            telegram_bot.answer_callback_query(call_id, "Sorry, you are not allowed to use this command. Please contact the bot owner for more information.", show_alert=True)
            return

        if data.startswith('settings_language'):
            if data == 'settings_language_en':
                SetLanguage(user_id, 'en')
                telegram_bot.answer_callback_query(call_id, f"Bot language was set to English")

            elif data == 'settings_language_ru':
                SetLanguage(user_id, 'ru')
                telegram_bot.answer_callback_query(call_id, f"Bot language was set to Russian")

            telegram_bot.edit_message_text(f"Which language do you want to choose for the bot?",
                                           chat_id, message_id, reply_markup=GenKBLanguageSettings())
            
        elif data.startswith('settings_model'):
            if data == 'settings_model_gpt35':
                SetModel(user_id, 'gpt-3.5-turbo')
                telegram_bot.answer_callback_query(call_id, f"Chat model for the bot was set to gpt-3.5-turbo")
            elif data == 'settings_model_gpt4':
                SetModel(user_id, 'gpt-4')
                telegram_bot.answer_callback_query(call_id, f"Chat model for the bot was set to gpt-4")
                
            telegram_bot.edit_message_text(f"Which chat model do you want to choose for the bot?",
                                           chat_id, message_id, reply_markup=GenKBModelSettings())
            
        else:
            telegram_bot.edit_message_text(f"Which settings do you want to change for the bot?",
                                           chat_id, message_id, reply_markup=GenKBSettings())

    elif data.startswith('manage'):
        if GetCategory(user_id) != 'owner':
            telegram_bot.answer_callback_query(call_id, "Sorry, you are not allowed to use this command. Please contact the bot owner for more information.", show_alert=True)
            return

        if data == 'manage_admins':
            telegram_bot.edit_message_text("Managing admins of the Bot:",
                                           chat_id, message_id, reply_markup=GenKBAdmins())
        elif data == 'manage_users':
            telegram_bot.edit_message_text("Managing users of the Bot:",
                                           chat_id, message_id, reply_markup=GenKBUsers())
        elif data == 'manage_banned':
            telegram_bot.edit_message_text("Managing banned users of the Bot:",
                                           chat_id, message_id, reply_markup=GenKBBannedUsers())
        
        elif data.startswith('manage_admin_'):
            user_id = int(data.split('_')[-1])
            telegram_bot.edit_message_text(f"What do you want to do for the admin @{GetName(user_id)}?",
                                           chat_id, message_id, reply_markup=GenKBAdmin(user_id))
        elif data.startswith('manage_user_'):
            user_id = int(data.split('_')[-1])
            telegram_bot.edit_message_text(f"What do you want to do for the user @{GetName(user_id)}?",
                                           chat_id, message_id, reply_markup=GenKBUser(user_id))
        elif data.startswith('manage_banned_'):
            user_id = int(data.split('_')[-1])
            telegram_bot.edit_message_text(f"What do you want to do with the banned user @{GetName(user_id)}?",
                                           chat_id, message_id, reply_markup=GenKBBanned(user_id))
        
        elif data.startswith('manage_role_'):
            user_id = int(data.split('_')[-1])

            if data.startswith('manage_role_admin_'):
                SetCategory(user_id, 'admin')
                telegram_bot.answer_callback_query(call_id, f"User @{GetName(user_id)} is now an Admin of the Bot", show_alert=True)
            elif data.startswith('manage_role_user_'):
                SetCategory(user_id, 'user')
                telegram_bot.answer_callback_query(call_id, f"User @{GetName(user_id)} is now a User of the Bot", show_alert=True)
            elif data.startswith('manage_role_banned_'):
                SetCategory(user_id, 'banned')
                telegram_bot.answer_callback_query(call_id, f"User @{GetName(user_id)} is now a Banned User of the Bot", show_alert=True)
            
            telegram_bot.edit_message_text("Let's manage the users of the Bot:",
                                           chat_id, message_id, reply_markup=GenKBUserCategoties())

        elif data.startswith('manage_language_'):
            user_id = int(data.split('_')[-1])
            
            if data.startswith('manage_language_en_'):
                SetLanguage(user_id, 'en')
                telegram_bot.answer_callback_query(call_id, f"Bot language for the user @{GetName(user_id)} was set to English")
            elif data.startswith('manage_language_ru_'):
                SetLanguage(user_id, 'ru')
                telegram_bot.answer_callback_query(call_id, f"Bot language for the user @{GetName(user_id)} was set to Russian")
            
            telegram_bot.edit_message_text(f"Which language do you want to choose for the user @{GetName(user_id)}?\n" +
                                           f"(Current language: {GetLanguage(user_id)})",
                                           chat_id, message_id, reply_markup=GenKBLanguage(user_id))
        
        elif data.startswith('manage_model_'):
            user_id = int(data.split('_')[-1])

            if data.startswith('manage_model_gpt35_'):
                SetModel(user_id, 'gpt-3.5-turbo')
                telegram_bot.answer_callback_query(call_id, f"Bot model for the user @{GetName(user_id)} was set to gpt-3.5-turbo")
            elif data.startswith('manage_model_gpt4_'):
                SetModel(user_id, 'gpt-4')
                telegram_bot.answer_callback_query(call_id, f"Bot model for the user @{GetName(user_id)} was set to gpt-4")
            
            telegram_bot.edit_message_text(f"Which model do you want to choose for the user @{GetName(user_id)}?\n" +
                                           f"(Current model: {GetModel(user_id)})",
                                           chat_id, message_id, reply_markup=GenKBModel(user_id))

        elif data.startswith('manage_budget_'):
            user_id = int(data.split('_')[-1])
            
            if data.startswith('manage_budget_increase_'):
                SetBudget(user_id, Decimal(GetBudget(user_id)) + Decimal(0.1))
                telegram_bot.answer_callback_query(call_id, f"Bot budget for the user @{GetName(user_id)} was increased by 0.1$ and is now {GetBudget(user_id)}$")
            elif data.startswith('manage_budget_decrease_'):
                if GetBudget(user_id) > Decimal(0.1):
                    SetBudget(user_id, Decimal(GetBudget(user_id)) - Decimal(0.1))
                    telegram_bot.answer_callback_query(call_id, f"Bot budget for the user @{GetName(user_id)} was decreased by 0.1$ and is now {GetBudget(user_id)}$")
                else:
                    SetBudget(user_id, Decimal(0))
                    telegram_bot.answer_callback_query(call_id, f"Bot budget for the user @{GetName(user_id)} was set to 0$")
                    
            telegram_bot.edit_message_text(f"What do you want to do with the budget of the user @{GetName(user_id)}?\n" +
                                           f"(Current budget: {GetBudget(user_id)})",
                                           chat_id, message_id, reply_markup=GenKBBudget(user_id))
        
        elif data.startswith('manage_delete_'):
            user_id = int(data.split('_')[-1])
            
            if data.startswith('manage_delete_admin_'):
                telegram_bot.edit_message_text(f"Do you want to delete the user @{GetName(user_id)} (is now an Admin) from the database of the Bot?",
                                               chat_id, message_id, reply_markup=GenKBDeleteAdmin(user_id))
            elif data.startswith('manage_delete_user_'):
                telegram_bot.edit_message_text(f"Do you want to delete the user @{GetName(user_id)} (is now a User) from the database of the Bot?",
                                               chat_id, message_id, reply_markup=GenKBDeleteUser(user_id))
            else:
                telegram_bot.edit_message_text(f"Do you want to delete the user @{GetName(user_id)} (is now a Banned User) from the database of the Bot?",
                                               chat_id, message_id, reply_markup=GenKBDeleteBanned(user_id))
            
        elif data.startswith('manage_remove_'):
            user_id = int(data.split('_')[-1])
            
            DeleteUserInfo(user_id)
            telegram_bot.answer_callback_query(call_id, f"User @{GetName(user_id)} was totally deleted from the database of the Bot", show_alert=True)
            
            if data.startswith('manage_remove_admin_'):
                telegram_bot.edit_message_text("Managing admins of the Bot:",
                                               chat_id, message_id, reply_markup=GenKBAdmins())
            elif data.startswith('manage_remove_user_'):
                telegram_bot.edit_message_text("Managing users of the Bot:",
                                               chat_id, message_id, reply_markup=GenKBUsers())
            else:
                telegram_bot.edit_message_text("Managing banned users of the Bot:",
                                               chat_id, message_id, reply_markup=GenKBBannedUsers())

        else:
            telegram_bot.edit_message_text("Let's manage the users of the Bot:",
                                           chat_id, message_id, reply_markup=GenKBUserCategoties())

    else:
        telegram_bot.answer_callback_query(call_id, "Something went wrong inside the bot. Try to repeat the command later or contact the bot owner for more information.", show_alert=True)