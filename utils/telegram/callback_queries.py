from decimal import Decimal
from logging import Logger
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup

import utils.telegram.keyboards as kb_gen
import utils.telegram.callback_queries_settings
import utils.telegram.callback_queries_users
import utils.openai.helper
from utils.users import UserInfo
from utils.translations import GetTranslation as Translate
from utils.system_prompts import GetSystemPrompt
from utils.yandexcloud.user_management import GetUserByID, SetUserLanguage
from utils.telegram.callback_queries_settings import (
    HandleModelChatCallbackQuery, HandleModelVisionCallbackQuery, HandleModelImageCallbackQuery,
    HandleModelTranslateCallbackQuery, HandleModelTranscribeCallbackQuery, HandleModelSyntesizeCallbackQuery,
    HandleTemperatureCallbackQuery, HandleTokenLimitCallbackQuery,
)
from utils.telegram.callback_queries_users import (
    HandleUserCategotiesCallbackQuery, HandleManageUserCallbackQuery,
    HandleManageRoleCallbackQuery, HandleManageLanguageCallbackQuery, HandleManageSettingsCallbackQuery,
    HandleManageModelCallbackQuery, HandleManageTemperatureCallbackQuery, HandleManageTokenLimitCallbackQuery,
    HandleManageBudgetCallbackQuery, HandleManageDeleteCallbackQuery, HandleManageRemoveCallbackQuery,
)

# Define services
logger: Logger

# Setup logger
def SetupLogger(external_logger: Logger):
    global logger

    logger = external_logger
    utils.telegram.callback_queries_settings.logger = logger
    utils.telegram.callback_queries_users.logger = logger

# Handle language callback query
def HandleLanguageCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo) -> UserInfo:
    if len(data) != 2:
        HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
        return user_info
    
    new_language = data[1].lower()

    if new_language == user_info['bot_language']:
        bot.answer_callback_query(
            callback_query_id=call_id,
            text=Translate(new_language, 'warning_same_language'),
            show_alert=True,
        )
        logger.info(f"User #{user_id} tried to set the bot language to the same language as the current one ('{new_language}')")
        return user_info

    if not SetUserLanguage(user_id, new_language):
        HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
        return user_info

    user_info['bot_language'] = new_language

    bot.send_message(
        chat_id=user_info['chat_id'],
        text=Translate(new_language, 'success_changed_language'),
    )

    bot.edit_message_text(
        text=f"{Translate(new_language, 'command_message_language')} ({Translate(new_language, 'current_value')} {Translate(new_language, 'language')})",
        chat_id=user_info['chat_id'],
        message_id=message_id,
        reply_markup=kb_gen.Language(),
    )

    logger.info(f"Successfully changed the bot language for user #{user_id} to '{new_language}'")
    
    return user_info

# Handle settings callback query
def HandleSettingsCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo) -> UserInfo:
    if len(data) == 1:
        bot.edit_message_text(
            text=Translate(user_info['bot_language'], 'command_message_settings'),
            chat_id=user_info['chat_id'],
            message_id=message_id,
            reply_markup=kb_gen.Settings(user_info['bot_language']),
        )
        logger.info(f"Opened the settings menu for user #{user_id}")
        return user_info
    
    section = data[1].lower()
    if section == 'model':
        if len(data) == 2:
            HandleUnknownCallbackQuery(bot, call_id, 'settings_model', user_id, user_info)
            return user_info
        
        model = data[2].lower()

        if model == 'chat':
            return HandleModelChatCallbackQuery(bot, call_id, data, message_id, user_id, user_info)
        elif model == 'vision':
            return HandleModelVisionCallbackQuery(bot, call_id, data, message_id, user_id, user_info)
        elif model == 'image':
            return HandleModelImageCallbackQuery(bot, call_id, data, message_id, user_id, user_info)
        elif model == 'translate':
            return HandleModelTranslateCallbackQuery(bot, call_id, data, message_id, user_id, user_info)
        elif model == 'transcribe':
            return HandleModelTranscribeCallbackQuery(bot, call_id, data, message_id, user_id, user_info)
        elif model == 'syntesize':
            return HandleModelSyntesizeCallbackQuery(bot, call_id, data, message_id, user_id, user_info)
    
    elif section == 'temperature':
        return HandleTemperatureCallbackQuery(bot, call_id, data, message_id, user_id, user_info)

    elif section == 'token':
        if len(data) > 2 and data[2].lower() == 'limit':
            return HandleTokenLimitCallbackQuery(bot, call_id, data, message_id, user_id, user_info)

    HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
    return user_info

# Handle reset callback query
def HandleResetCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo) -> UserInfo:
    if len(data) == 2:
        system_prompt = GetSystemPrompt(data[1].lower(), user_info['bot_language'])
        if system_prompt is not None:
            utils.openai.helper.ResetConversation(
                user_id=user_id,
                chat_id=user_info['chat_id'],
                system_prompt=system_prompt,
            )

            bot.edit_message_text(
                text=Translate(user_info['bot_language'], 'success_system_prompt') + '\n\n' + system_prompt,
                chat_id=user_info['chat_id'],
                message_id=message_id,
                reply_markup=InlineKeyboardMarkup(),
            )

            logger.info(f"Successfully reset the conversation history for user #{user_id}")

            return user_info
    
    HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
    return user_info

# Handle user management callback query
def HandleManagementCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo) -> UserInfo:
    if len(data) == 1:
        if data[0].lower() != 'manage':
            HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
            return user_info

        bot.edit_message_text(
            text=Translate(user_info['bot_language'], 'command_message_users'),
            chat_id=user_info['chat_id'],
            message_id=message_id,
            reply_markup=kb_gen.Users(user_info['bot_language']),
        )
        return user_info
    
    section = data[1].lower()
    if len(data) == 2 and section in ('admins', 'users', 'banned', ):
        return HandleUserCategotiesCallbackQuery(bot, call_id, message_id, user_id, user_info, section)
    
    manage_user_id = data[-1].lower()
    if not manage_user_id.isnumeric():
        HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
        return user_info
    
    manage_user_id = Decimal(manage_user_id)
    manage_user = GetUserByID(manage_user_id)
    if manage_user is None:
        HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
        return user_info
    
    manage_user_info = UserInfo(manage_user['info'])

    if len(data) == 2:
        return HandleManageUserCallbackQuery(bot, call_id, message_id, user_id, user_info, manage_user_id, manage_user_info)
    
    match section:
        case 'role':
            return HandleManageRoleCallbackQuery(bot, call_id, data, message_id, user_id, user_info, manage_user_id, manage_user_info)
        case 'language':
            return HandleManageLanguageCallbackQuery(bot, call_id, data, message_id, user_id, user_info, manage_user_id, manage_user_info)
        case 'settings':
            return HandleManageSettingsCallbackQuery(bot, call_id, data, message_id, user_id, user_info, manage_user_id, manage_user_info)
        case 'model':
            return HandleManageModelCallbackQuery(bot, call_id, data, message_id, user_id, user_info, manage_user_id, manage_user_info)
        case 'temperature':
            return HandleManageTemperatureCallbackQuery(bot, call_id, data, message_id, user_id, user_info, manage_user_id, manage_user_info)
        case 'token':
            return HandleManageTokenLimitCallbackQuery(bot, call_id, data, message_id, user_id, user_info, manage_user_id, manage_user_info)
        case 'budget':
            return HandleManageBudgetCallbackQuery(bot, call_id, data, message_id, user_id, user_info, manage_user_id, manage_user_info)
        case 'delete':
            return HandleManageDeleteCallbackQuery(bot, call_id, data, message_id, user_id, user_info, manage_user_id, manage_user_info)
        case 'remove':
            return HandleManageRemoveCallbackQuery(bot, call_id, data, message_id, user_id, user_info, manage_user_id, manage_user_info)
        case _:
            HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
            return user_info

# Handle unknown callback query
def HandleUnknownCallbackQuery(bot: TeleBot, call_id: int, call_data: list[str], user_id: int, user_info: UserInfo):
    data = '_'.join(call_data)

    bot.answer_callback_query(
        callback_query_id=call_id,
        text=Translate(user_info['bot_language'], 'error_callback_query'),
        show_alert=True,
    )

    bot.send_message(
        chat_id=user_info['chat_id'],
        text=Translate(user_info['bot_language'], 'error_callback_query'),
    )

    logger.error(f"Error processing callback query '{data}' for user #{user_id}: unsupported callback query")