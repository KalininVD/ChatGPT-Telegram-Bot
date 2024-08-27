# Import necessary modules, classes and functions
from decimal import Decimal
from telebot import TeleBot, logger
from telebot.types import Message, CallbackQuery, ReplyParameters
from utils.translations import get_translation as Translate
from utils.openai import OpenAIHelper
from utils.plugins import PluginManager
import utils.inline_keyboards as kb_gen
from utils.telegram import (
    GetName, GetCategory, GetLanguage, GetModel, GetBudget,
    SetName, SetCategory, SetLanguage, SetModel, SetBudget,
    DeleteUserInfo, GetBaseCommands
)
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

    openai_helper = OpenAIHelper(logger)
    plugin_manager = PluginManager()

# Initialize the bot
def InitBot(vars: dict) -> TeleBot:
    if any(var not in vars for var in ('TELEGRAM_BOT_TOKEN', 'OWNER_TELEGRAM_ID', 'OWNER_TELEGRAM_NAME')):
        raise ValueError(Translate("en", "env_vars_error"))

    bot = TeleBot(vars['TELEGRAM_BOT_TOKEN'])
    bot.set_my_commands(commands=GetBaseCommands())

    SetCategory(vars['OWNER_TELEGRAM_ID'], 'owner')
    SetName(vars['OWNER_TELEGRAM_ID'], vars['OWNER_TELEGRAM_NAME'])
    SetBudget(vars['OWNER_TELEGRAM_ID'], Decimal('100')) # Put your budget here (Infinity is not supported yet...)

    return bot

def is_recognized_command(command: str) -> bool:
    recognized_commands = [
        '/start', '/help', '/language', '/budget', '/reset', '/summarize', '/settings', '/users'
    ]
    return command in recognized_commands

# Handle incoming messages
def HandleMessage(bot: TeleBot, message: Message):
    user_id = message.from_user.id

    if GetCategory(user_id) in ('banned', 'unknown'):
        bot.send_message(
            chat_id=message.chat.id,
            text=Translate(GetLanguage(message.from_user.id), "banned_response")
        )
        return

    # Log the incoming message details
    logger.info(f"Received {message.content_type} message from user {user_id}: {len(message.text)} characters long")

    if message.content_type == 'text' and message.text.startswith('/'):  # Check if it's a command
        if not is_recognized_command(message.text):  # Check for unrecognized command
            logger.warning(f"Unrecognized command received from user {user_id}: {message.text}")
            bot.reply_to(message, Translate(GetLanguage(user_id), "unknown_command_response"))
            return

    try:
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
                bot.reply_to(message, Translate(GetLanguage(user_id), "unknown_message_type"))

    except Exception as e:
        logger.error(f"Error processing message from user {user_id}: {str(e)}", exc_info=True)
        bot.reply_to(message, Translate(GetLanguage(user_id), "error_processing_message"))

# Handle text messages
def HandleTextMessage(bot: TeleBot, message: Message):
    user_id = message.from_user.id
    user_message = message.text

    logger.info(f"Received message from user {user_id}: {len(user_message)} characters long")

    budget = GetBudget(user_id)
    budget_exceeded = budget <= Decimal(0)
    if not budget_exceeded:
        try:
            model = GetModel(user_id)

            # Call the OpenAI API through the OpenAIHelper
            response, usage = openai_helper.get_text_response(
                user_id=user_id,
                message=user_message,
                model_name=model
            )

            # Calculate the cost of the response and change the budget
            cost = openai_helper.calculate_text_cost(usage, model)
            budget_exceeded = cost > budget
            SetBudget(user_id, budget - cost)

            # Send the response back to the user
            bot.send_message(
                chat_id=message.chat.id,
                reply_parameters=ReplyParameters(message_id=message.message_id),
                text=response
            )

            logger.info(f"Sent response to user {user_id}: {len(response)} characters long")

        except Exception as e:
            logger.error(f"Error processing message for user {user_id}: {str(e)}", exc_info=True)
            bot.reply_to(message, Translate(GetLanguage(user_id), "error_processing_message"))
    
    # Send a message to the user if he has exceeded his budget
    if budget_exceeded:
        bot.send_message(
            chat_id=message.chat.id,
            text=Translate(GetLanguage(user_id), "budget_exceeded")
        )

        logger.warning(f"User {user_id} has exceeded his budget")

# Handle photo messages
def HandlePhotoMessage(bot: TeleBot, message: Message):
    logger.info(f"Received photo message from user {message.from_user.id}")
    bot.send_message(
        chat_id=message.chat.id,
        reply_parameters=ReplyParameters(message_id=message.message_id),
        text="This type of message is not supported yet"
    )

# Handle audio messages
def HandleAudioMessage(bot: TeleBot, message: Message):
    logger.info(f"Received audio message from user {message.from_user.id}")
    bot.send_message(
        chat_id=message.chat.id,
        reply_parameters=ReplyParameters(message_id=message.message_id),
        text="This type of message is not supported yet"
    )

# Handle voice messages
def HandleVoiceMessage(bot: TeleBot, message: Message):
    logger.info(f"Received voice message from user {message.from_user.id}")
    bot.send_message(
        chat_id=message.chat.id,
        reply_parameters=ReplyParameters(message_id=message.message_id),
        text="This type of message is not supported yet"
    )

# Handle video messages
def HandleVideoMessage(bot: TeleBot, message: Message):
    logger.info(f"Received video message from user {message.from_user.id}")
    bot.send_message(
        chat_id=message.chat.id,
        reply_parameters=ReplyParameters(message_id=message.message_id),
        text="This type of message is not supported yet"
    )

# Handle video note messages
def HandleVideoNoteMessage(bot: TeleBot, message: Message):
    logger.info(f"Received video note message from user {message.from_user.id}")
    bot.send_message(
        chat_id=message.chat.id,
        reply_parameters=ReplyParameters(message_id=message.message_id),
        text="This type of message is not supported yet"
    )

# Handle document messages
def HandleDocumentMessage(bot: TeleBot, message: Message):
    logger.info(f"Received document message from user {message.from_user.id}")
    bot.send_message(
        chat_id=message.chat.id,
        reply_parameters=ReplyParameters(message_id=message.message_id),
        text="This type of message is not supported yet"
    )

# Handle dice messages
def HandleDiceMessage(bot: TeleBot, message: Message):
    logger.info(f"Received dice message from user {message.from_user.id}")
    bot.send_message(
        chat_id=message.chat.id,
        reply_parameters=ReplyParameters(message_id=message.message_id),
        text="This type of message is not supported yet"
    )


# Send a start message to the user
def Start(bot: TeleBot, message: Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=Translate(GetLanguage(message.from_user.id), "start_message")
    )

# Send a help message to the user
def Help(bot: TeleBot, message: Message):
    lang = GetLanguage(message.from_user.id)

    help_message = Translate(lang, "help_message_start")

    help_message += f"/start - {Translate(lang, 'start_command_description')}\n"
    help_message += f"/help - {Translate(lang, 'help_command_description')}\n"
    help_message += f"/language - {Translate(lang, 'language_command_description')}\n"
    help_message += f"/budget - {Translate(lang, 'budget_command_description')}\n"

    if GetCategory(message.from_user.id) in ('owner', 'admin', 'user'):
        help_message += f"/reset - {Translate(lang, 'reset_command_description')}\n"
        help_message += f"/summarize - {Translate(lang, 'summarize_command_description')}\n"

    if GetCategory(message.from_user.id) in ('owner', 'admin'):
        help_message += f"/settings - {Translate(lang, 'settings_command_description')}\n"

    if GetCategory(message.from_user.id) in ('owner'):
        help_message += f"/users - {Translate(lang, 'users_command_description')}\n"

    help_message += Translate(lang, "help_message_end")

    bot.send_message(
        chat_id=message.chat.id,
        text=help_message
    )

# Change the bot's language for the user
def Language(bot: TeleBot, message: Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=Translate(GetLanguage(message.from_user.id), "language_command_text"),
        reply_markup=kb_gen.LanguageGeneral()
    )

# Get the bot's budget for the user
def Budget(bot: TeleBot, message: Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=f"{Translate(GetLanguage(message.from_user.id), 'budget_command_text')} {GetBudget(message.from_user.id)}$"
    )

# Reset the conversation history
def Reset(bot: TeleBot, message: Message):
    lang = GetLanguage(message.from_user.id)

    if GetCategory(message.from_user.id) not in ('owner', 'admin', 'user'):
        bot.send_message(
            chat_id=message.chat.id,
            text=Translate(lang, "command_disallowed_message")
        )
        return
    
    openai_helper.reset_conversation(message.from_user.id)

    bot.send_message(
        chat_id=message.chat.id,
        text=Translate(lang, "reset_command_text")
    )

# Summarize the conversation
def Summarize(bot: TeleBot, message: Message):
    lang = GetLanguage(message.from_user.id)

    if GetCategory(message.from_user.id) not in ('owner', 'admin', 'user'):
        bot.send_message(
            chat_id=message.chat.id,
            text=Translate(lang, "command_disallowed_message")
        )
        return

    bot.send_message(
        chat_id=message.chat.id,
        text=Translate(lang, "summarize_command_text")
    )

# Get the bot's settings
def Settings(bot: TeleBot, message: Message):
    lang = GetLanguage(message.from_user.id)

    if GetCategory(message.from_user.id) not in ('owner', 'admin'):
        bot.send_message(
            chat_id=message.chat.id,
            text=Translate(lang, "command_disallowed_message")
        )
        return

    bot.send_message(
        chat_id=message.chat.id,
        text=Translate(lang, "settings_command_text"),
        reply_markup=kb_gen.Settings(lang)
    )

# Manage users and admins of the bot
def Users(bot: TeleBot, message: Message):
    lang = GetLanguage(message.from_user.id)

    if GetCategory(message.from_user.id) != 'owner':
        bot.send_message(
            chat_id=message.chat.id,
            text=Translate(lang, "command_disallowed_message")
        )
        return

    bot.send_message(
        chat_id=message.chat.id,
        text=Translate(lang, "users_command_text"),
        reply_markup=kb_gen.UserCategoties(lang)
    )


# Handle the callback query
def HandleCallbackQuery(bot: TeleBot, call: CallbackQuery):
    data = call.data
    user_id = call.from_user.id
    lang = GetLanguage(user_id)

    inform, edit = None, False
    answer, text = '', ''
    keyboard = None

    if data == 'language':
        edit = True
        text = Translate(lang, "language_command_text")
        keyboard = kb_gen.LanguageGeneral()
    elif data.startswith('language_'):
        inform = False
        if data == 'language_ru':
            lang = "ru"
        else:
            lang = "en"

        SetLanguage(user_id, lang)

        answer = f"{Translate(lang, 'language_changed')} {Translate(lang, 'language')}"

        edit = True
        text = Translate(lang, "language_command_text")
        keyboard = kb_gen.LanguageGeneral()

    elif GetCategory(user_id) in ('unknown', 'banned', 'user'):
        inform = True
        answer = Translate(lang, "command_disallowed_message")

    elif data == 'settings':
        edit = True
        text = Translate(lang, "settings_command_text")
        keyboard = kb_gen.Settings(lang)
    elif data.startswith('settings_'):
        if data == 'settings_language':
            edit = True
            text = Translate(lang, "language_command_text")
            keyboard = kb_gen.LanguageSettings(lang)
        elif data.startswith('settings_language_'):
            inform = False
            if data == 'settings_language_ru':
                lang = "ru"
            else:
                lang = "en"

            SetLanguage(user_id, lang)

            answer = f"{Translate(lang, 'language_changed')} {Translate(lang, 'language')}"

            edit = True
            text = Translate(lang, "language_command_text")
            keyboard = kb_gen.LanguageSettings(lang)

        elif data == 'settings_model':
            edit = True
            text = Translate(lang, "chat_model_choice")
            keyboard = kb_gen.ModelSettings(lang)
        elif data.startswith('settings_model_'):
            inform = False
            model = data.split('_')[-1]
            if SetModel(user_id, model):
                answer = f"{Translate(lang, 'chat_model_changed')} {model}"
            else:
                SetModel(user_id, 'gpt-4o-mini')
                answer = f"{Translate(lang, 'chat_model_changed')} GPT-4o-mini"

        else:
            inform = True
            answer = Translate(lang, "callback_query_error")

    elif GetCategory(user_id) == 'admin':
        inform = True
        answer = Translate(lang, "command_disallowed_message")

    elif data == 'manage':
        edit = True
        text = Translate(lang, "users_command_text")
        keyboard = kb_gen.UserCategoties(lang)
    elif data.startswith('manage_'):
        edit = True
        if data == 'manage_admins':
            text = f"{Translate(lang, 'managing_start')} {Translate(lang, 'admins').lower()} {Translate(lang, 'managing_end')}"
            keyboard = kb_gen.Admins(lang)
        elif data == 'manage_users':
            text = f"{Translate(lang, 'managing_start')} {Translate(lang, 'users').lower()} {Translate(lang, 'managing_end')}"
            keyboard = kb_gen.Users(lang)
        elif data == 'manage_banned':
            text = f"{Translate(lang, 'managing_start')} {Translate(lang, 'banned_users').lower()} {Translate(lang, 'managing_end')}"
            keyboard = kb_gen.BannedUsers(lang)
        else:
            try:
                user_id = int(data.split('_')[-1])
                user_name = GetName(user_id)
                data = '_'.join(data.split('_')[:-1])
            except ValueError:
                data = 'error'

            if data == 'manage_admin':
                text = f"{Translate(lang, 'ask_manage')} {Translate(lang, 'admin').lower()} @{user_name}?"
                keyboard = kb_gen.Admin(user_id, lang)
            elif data == 'manage_user':
                text = f"{Translate(lang, 'ask_manage')} {Translate(lang, 'user').lower()} @{user_name}?"
                keyboard = kb_gen.User(user_id, lang)
            elif data == 'manage_banned':
                text = f"{Translate(lang, 'ask_manage')} {Translate(lang, 'banned').lower()} @{user_name}?"
                keyboard = kb_gen.Banned(user_id, lang)

            elif data.startswith('manage_role_'):
                inform = True
                text = Translate(lang, "users_command_text")
                keyboard = kb_gen.UserCategoties(lang)

                if data == 'manage_role_admin':
                    SetCategory(user_id, 'admin')
                    answer = f"{Translate(lang, 'user')} @{user_name} {Translate(lang, 'manage_role_start')} {Translate(lang, 'admin')} {Translate(lang, 'manage_role_end')}"
                elif data == 'manage_role_user':
                    SetCategory(user_id, 'user')
                    answer = f"{Translate(lang, 'user')} @{user_name} {Translate(lang, 'manage_role_start')} {Translate(lang, 'user')} {Translate(lang, 'manage_role_end')}"
                else:
                    SetCategory(user_id, 'banned')
                    answer = f"{Translate(lang, 'user')} @{user_name} {Translate(lang, 'manage_role_start')} {Translate(lang, 'banned')} {Translate(lang, 'manage_role_end')}"

            elif data == 'manage_language':
                edit = True
                text = f"{Translate(lang, 'manage_language_start')} {Translate(lang, 'user').lower()} @{user_name}{Translate(lang, 'manage_language_end')} {Translate(lang, f'language_button_{GetLanguage(user_id)}')})"
                keyboard = kb_gen.Language(user_id, lang)
            elif data.startswith('manage_language_'):
                inform = False
                if data == 'manage_language_ru':
                    SetLanguage(user_id, 'ru')
                else:
                    SetLanguage(user_id, 'en')

                answer = f"{Translate(lang, 'manage_language_successful_start')} {Translate(lang, 'user').lower()} @{user_name} {Translate(lang, 'manage_language_successful_end')} {Translate(lang, f'language_button_{GetLanguage(user_id)}')}"
                edit = True
                text = f"{Translate(lang, 'manage_language_start')} {Translate(lang, 'user').lower()} @{user_name}{Translate(lang, 'manage_language_end')} {Translate(lang, f'language_button_{GetLanguage(user_id)}')})"
                keyboard = kb_gen.Language(user_id, lang)

            elif data == 'manage_model':
                edit = True
                text = f"{Translate(lang, 'manage_model_start')} {Translate(lang, 'user').lower()} @{user_name}{Translate(lang, 'manage_model_end')} {GetModel(user_id)})"
                keyboard = kb_gen.Model(user_id, lang)
            elif data.startswith('manage_model_'):
                inform = False
                model = data.split('_')[-1]
                if SetModel(user_id, model):
                    answer = f"{Translate(lang, 'manage_model_successful_start')} {Translate(lang, 'user').lower()} @{user_name} {Translate(lang, 'manage_model_successful_end')} {model}"
                else:
                    SetModel(user_id, 'gpt-4o-mini')
                    answer = f"{Translate(lang, 'manage_model_successful_start')} {Translate(lang, 'user').lower()} @{user_name} {Translate(lang, 'manage_model_successful_end')} GPT-4o-mini"

                edit = True
                text = f"{Translate(lang, 'manage_model_start')} {Translate(lang, 'user').lower()} @{user_name}{Translate(lang, 'manage_model_end')} {GetModel(user_id)})"
                keyboard = kb_gen.Model(user_id, lang)

            elif data == 'manage_budget':
                edit = True
                text = f"{Translate(lang, 'manage_budget_start')} {Translate(lang, 'user').lower()} @{user_name}{Translate(lang, 'manage_budget_end')} {GetBudget(user_id)}$)"
                keyboard = kb_gen.Budget(user_id, lang)
            elif data.startswith('manage_budget_'):
                inform = False
                budget = GetBudget(user_id)
                if data == 'manage_budget_increase':
                    budget += Decimal('0.1')
                    answer = f"{Translate(lang, 'manage_budget_increased_start')} {Translate(lang, 'user').lower()} @{user_name} {Translate(lang, 'manage_budget_increased_end')} {budget}$"
                else:
                    if budget > Decimal(0.1):
                        budget -= Decimal('0.1')
                        answer = f"{Translate(lang, 'manage_budget_decreased_start')} {Translate(lang, 'user').lower()} @{user_name} {Translate(lang, 'manage_budget_decreased_end')} {budget}$"
                    else:
                        budget = Decimal(0)
                        answer = f"{Translate(lang, 'manage_budget_zero_start')} {Translate(lang, 'user').lower()} @{user_name} {Translate(lang, 'manage_budget_zero_end')}"

                SetBudget(user_id, budget)
                edit = True
                text = f"{Translate(lang, 'manage_budget_start')} {Translate(lang, 'user').lower()} @{user_name}{Translate(lang, 'manage_budget_end')} {budget}$)"
                keyboard = kb_gen.Budget(user_id, lang)

            elif data.startswith('manage_delete_'):
                edit = True
                if data == 'manage_delete_admin':
                    text = f"{Translate(lang, 'manage_delete_start')} {Translate(lang, 'admin').lower()} @{user_name} {Translate(lang, 'manage_delete_end')}"
                    keyboard = kb_gen.DeleteAdmin(user_id, lang)
                elif data == 'manage_delete_user':
                    text = f"{Translate(lang, 'manage_delete_start')} {Translate(lang, 'user').lower()} @{user_name} {Translate(lang, 'manage_delete_end')}"
                    keyboard = kb_gen.DeleteUser(user_id, lang)
                else:
                    text = f"{Translate(lang, 'manage_delete_start')} {Translate(lang, 'banned').lower()} @{user_name} {Translate(lang, 'manage_delete_end')}"
                    keyboard = kb_gen.DeleteBanned(user_id, lang)

            elif data.startswith('manage_remove_'):
                DeleteUserInfo(user_id)
                inform = True
                answer = f"{Translate(lang, 'user')} @{user_name} {Translate(lang, 'manage_removed')}"
                edit = True
                if data == 'manage_remove_admin':
                    text = f"{Translate(lang, 'managing_start')} {Translate(lang, 'admins').lower()} {Translate(lang, 'managing_end')}"
                    keyboard = kb_gen.Admins(lang)
                elif data == 'manage_remove_user':
                    text = f"{Translate(lang, 'managing_start')} {Translate(lang, 'users').lower()} {Translate(lang, 'managing_end')}"
                    keyboard = kb_gen.Users(lang)
                else:
                    text = f"{Translate(lang, 'managing_start')} {Translate(lang, 'banned_users').lower()} {Translate(lang, 'managing_end')}"
                    keyboard = kb_gen.BannedUsers(lang)

            else:
                inform = True
                answer = Translate(lang, "callback_query_error")
    else:
        inform = True
        answer = Translate(lang, "callback_query_error")

    if inform is not None:
        bot.answer_callback_query(
            callback_query_id=call.id,
            text=answer,
            show_alert=inform
        )

    if edit:
        bot.edit_message_text(
            text=text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=keyboard
        )