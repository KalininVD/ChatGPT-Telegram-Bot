from decimal import Decimal
from logging import Logger
from telebot import TeleBot

import utils.telegram.keyboards as kb_gen
from utils.users import UserInfo
from utils.telegram.commands import UpdateBotCommands
from utils.translations import GetTranslation as Translate
from utils.yandexcloud.user_management import (
    SetUserLanguage, SetUserRole, SetUserBudget,
    SetUserChatModel, SetUserVisionModel, SetUserImageModel,
    SetUserTranslateModel, SetUserSTTModel, SetUserTTSModel,
    SetUserTemperature, SetUserTokenLimit, DeleteUser,
)

# Define services
logger: Logger

# Handle callback query for managing users of the specified category
def HandleUserCategotiesCallbackQuery(bot: TeleBot, call_id: int, message_id: int, user_id: int, user_info: UserInfo, section: str) -> UserInfo:
    language = user_info['bot_language']

    match section:
        case 'admins':
            bot.edit_message_text(
                text=Translate(language, 'manage_admins'),
                chat_id=user_info['chat_id'],
                message_id=message_id,
                reply_markup=kb_gen.UsersAdmins(language),
            )
            logger.info(f"Opened the admins menu for user #{user_id}")
        case 'users':
            bot.edit_message_text(
                text=Translate(language, 'manage_users'),
                chat_id=user_info['chat_id'],
                message_id=message_id,
                reply_markup=kb_gen.UsersUsers(language),
            )
            logger.info(f"Opened the users menu for user #{user_id}")
        case 'banned':
            bot.edit_message_text(
                text=Translate(language, 'manage_banned'),
                chat_id=user_info['chat_id'],
                message_id=message_id,
                reply_markup=kb_gen.UsersBanned(language),
            )
            logger.info(f"Opened the banned users menu for user #{user_id}")
        case _:
            HandleUnknownCallbackQuery(bot, call_id, f"manage_{section}", user_id, user_info)

    return user_info

# Handle manage any user management callback query
def HandleManageUserCallbackQuery(bot: TeleBot, call_id: int, message_id: int, user_id: int, user_info: UserInfo, manage_user_id: int, manage_user_info: UserInfo) -> UserInfo:
    language = user_info['bot_language']

    match manage_user_info['user_role']:
        case 'admin':
            bot.edit_message_text(
                text=f"{Translate(language, 'manage_admin_ask')}{manage_user_info['user_name']}?",
                chat_id=user_info['chat_id'],
                message_id=message_id,
                reply_markup=kb_gen.UsersAdmin(manage_user_id, language),
            )
            logger.info(f"Opened the admin #{manage_user_id} menu for user #{user_id}")
        case 'user':
            bot.edit_message_text(
                text=f"{Translate(language, 'manage_user_ask')}{manage_user_info['user_name']}?",
                chat_id=user_info['chat_id'],
                message_id=message_id,
                reply_markup=kb_gen.UsersUser(manage_user_id, language),
            )
            logger.info(f"Opened the user #{manage_user_id} menu for user #{user_id}")
        case 'banned':
            bot.edit_message_text(
                text=f"{Translate(language, 'manage_banned_ask')}{manage_user_info['user_name']}?",
                chat_id=user_info['chat_id'],
                message_id=message_id,
                reply_markup=kb_gen.UsersBannedUser(manage_user_id, language),
            )
            logger.info(f"Opened the banned user #{manage_user_id} menu for user #{user_id}")
        case _:
            HandleUnknownCallbackQuery(bot, call_id, f"manage_{manage_user_id}", user_id, user_info)

    return user_info

# Handle callback query for managing the user's role
def HandleManageRoleCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo, manage_user_id: int, manage_user_info: UserInfo) -> UserInfo:
    language = user_info['bot_language']

    if len(data) == 3:
        bot.edit_message_text(
            text=f"{Translate(language, f"manage_{manage_user_info['user_role']}_role")}{manage_user_info['user_name']}?",
            chat_id=user_info['chat_id'],
            message_id=message_id,
            reply_markup=kb_gen.UsersRole(manage_user_id, language),
        )
        logger.info(f"Opened the user #{manage_user_id} role menu for user #{user_id}")
        return user_info
    elif len(data) == 4:
        role = data[2].lower()
        if SetUserRole(manage_user_id, role):
            bot.answer_callback_query(
                callback_query_id=call_id,
                text=f"@{manage_user_info['user_name']} {Translate(language, f"manage_role_{role}_success")}",
                show_alert=True,
            )
            if role != manage_user_info['user_role']:
                UpdateBotCommands(bot, manage_user_info['chat_id'], role, manage_user_info['bot_language'])
                bot.edit_message_text(
                    text=f"{Translate(language, f"manage_{role}_role")}{manage_user_info['user_name']}?",
                    chat_id=user_info['chat_id'],
                    message_id=message_id,
                    reply_markup=kb_gen.UsersRole(manage_user_id, language),
                )
            logger.info(f"Successfully changed the user #{manage_user_id} role to '{role}' by user #{user_id}")
            return user_info
    
    HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
    return user_info

# Handle callback query for managing the user's language
def HandleManageLanguageCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo, manage_user_id: int, manage_user_info: UserInfo) -> UserInfo:
    language = user_info['bot_language']

    lang = manage_user_info['bot_language']

    if len(data) == 3:
        bot.edit_message_text(
            text=f"{Translate(language, f"manage_{manage_user_info['user_role']}_language")}{manage_user_info['user_name']}? ({Translate(language, 'current_value')} {Translate(language, f"button_language_{lang}")})",
            chat_id=user_info['chat_id'],
            message_id=message_id,
            reply_markup=kb_gen.UsersLanguage(manage_user_id, language),
        )
        logger.info(f"Opened the user #{manage_user_id} language menu for user #{user_id}")
        return user_info
    elif len(data) == 4:
        lang = data[2].lower()
        if SetUserLanguage(manage_user_id, lang):
            bot.answer_callback_query(
                callback_query_id=call_id,
                text=f"{Translate(language, f"manage_{manage_user_info['user_role']}_language_success")}{manage_user_info['user_name']} {Translate(language, f"manage_language_success_{lang}")}",
                show_alert=True,
            )
            if lang != manage_user_info['bot_language']:
                UpdateBotCommands(bot, manage_user_info['chat_id'], manage_user_info['user_role'], lang)
                bot.edit_message_text(
                    text=f"{Translate(language, f"manage_{manage_user_info['user_role']}_language")}{manage_user_info['user_name']}? ({Translate(language, 'current_value')} {Translate(language, f"button_language_{lang}")})",
                    chat_id=user_info['chat_id'],
                    message_id=message_id,
                    reply_markup=kb_gen.UsersLanguage(manage_user_id, language),
                )
            logger.info(f"Successfully changed the user #{manage_user_id} language to '{lang}' by user #{user_id}")
            return user_info
    
    HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
    return user_info

# Handle callback query for managing the user's settings
def HandleManageSettingsCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo, manage_user_id: int, manage_user_info: UserInfo) -> UserInfo:
    language = user_info['bot_language']

    if len(data) == 3:
        bot.edit_message_text(
            text=f"{Translate(language, 'manage_settings')}{manage_user_info['user_name']}?",
            chat_id=user_info['chat_id'],
            message_id=message_id,
            reply_markup=kb_gen.UsersSettings(manage_user_id, language),
        )
        logger.info(f"Opened the user #{manage_user_id} settings menu for user #{user_id}")
        return user_info

    HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
    return user_info


# Handle callback query for managing the user's models
def HandleManageModelCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo, manage_user_id: int, manage_user_info: UserInfo) -> UserInfo:
    if len(data) == 3:
        HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
        return user_info
    
    match data[2].lower():
        case 'chat':
            return HandleManageChatModelCallbackQuery(bot, call_id, data, message_id, user_id, user_info, manage_user_id, manage_user_info)
        case 'vision':
            return HandleManageVisionModelCallbackQuery(bot, call_id, data, message_id, user_id, user_info, manage_user_id, manage_user_info)
        case 'image':
            return HandleManageImageModelCallbackQuery(bot, call_id, data, message_id, user_id, user_info, manage_user_id, manage_user_info)
        case 'translate':
            return HandleManageTranslateModelCallbackQuery(bot, call_id, data, message_id, user_id, user_info, manage_user_id, manage_user_info)
        case 'transcribe':
            return HandleManageSTTModelCallbackQuery(bot, call_id, data, message_id, user_id, user_info, manage_user_id, manage_user_info)
        case 'syntesize':
            return HandleManageTTSModelCallbackQuery(bot, call_id, data, message_id, user_id, user_info, manage_user_id, manage_user_info)
        case _:
            HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
            return user_info

# Handle callback query for managing the user's chat model
def HandleManageChatModelCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo, manage_user_id: int, manage_user_info: UserInfo) -> UserInfo:
    language = user_info['bot_language']

    if len(data) == 4:
        bot.edit_message_text(
            text=f"{Translate(language, 'manage_model_chat')}{manage_user_info['user_name']}? ({Translate(language, 'current_value')} {manage_user_info['chat_model']})",
            chat_id=user_info['chat_id'],
            message_id=message_id,
            reply_markup=kb_gen.UsersModelChat(manage_user_id, language),
        )
        logger.info(f"Opened the user #{manage_user_id} chat model menu for user #{user_id}")
        return user_info
    elif len(data) == 5:
        chat_model = data[3].lower()
        if SetUserChatModel(manage_user_id, chat_model):
            bot.answer_callback_query(
                callback_query_id=call_id,
                text=f"{Translate(language, 'manage_model_chat_success')}{manage_user_info['user_name']} {Translate(language, 'manage_settings_success')} {chat_model}",
                show_alert=True,
            )
            if chat_model != manage_user_info['chat_model']:
                bot.edit_message_text(
                    text=f"{Translate(language, 'manage_model_chat')}{manage_user_info['user_name']}? ({Translate(language, 'current_value')} {chat_model})",
                    chat_id=user_info['chat_id'],
                    message_id=message_id,
                    reply_markup=kb_gen.UsersModelChat(manage_user_id, language),
                )
            logger.info(f"Successfully changed the user #{manage_user_id} chat model to '{chat_model}' by user #{user_id}")
            return user_info

    HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
    return user_info

# Handle callback query for managing the user's vision model
def HandleManageVisionModelCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo, manage_user_id: int, manage_user_info: UserInfo) -> UserInfo:
    language = user_info['bot_language']

    if len(data) == 4:
        bot.edit_message_text(
            text=f"{Translate(language, 'manage_model_vision')}{manage_user_info['user_name']}? ({Translate(language, 'current_value')} {manage_user_info['vision_model']})",
            chat_id=user_info['chat_id'],
            message_id=message_id,
            reply_markup=kb_gen.UsersModelVision(manage_user_id, language),
        )
        logger.info(f"Opened the user #{manage_user_id} vision model menu for user #{user_id}")
        return user_info
    elif len(data) == 5:
        vision_model = data[3].lower()
        if SetUserVisionModel(manage_user_id, vision_model):
            bot.answer_callback_query(
                callback_query_id=call_id,
                text=f"{Translate(language, 'manage_model_vision_success')}{manage_user_info['user_name']} {Translate(language, 'manage_settings_success')} {vision_model}",
                show_alert=True,
            )
            if vision_model != manage_user_info['vision_model']:
                bot.edit_message_text(
                    text=f"{Translate(language, 'manage_model_vision')}{manage_user_info['user_name']}? ({Translate(language, 'current_value')} {vision_model})",
                    chat_id=user_info['chat_id'],
                    message_id=message_id,
                    reply_markup=kb_gen.UsersModelVision(manage_user_id, language),
                )
            logger.info(f"Successfully changed the user #{manage_user_id} vision model to '{vision_model}' by user #{user_id}")
            return user_info
    
    HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
    return user_info

# Handle callback query for managing the user's image model
def HandleManageImageModelCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo, manage_user_id: int, manage_user_info: UserInfo) -> UserInfo:
    language = user_info['bot_language']

    if len(data) == 4:
        bot.edit_message_text(
            text=f"{Translate(language, 'manage_model_image')}{manage_user_info['user_name']}? ({Translate(language, 'current_value')} {manage_user_info['image_model']})",
            chat_id=user_info['chat_id'],
            message_id=message_id,
            reply_markup=kb_gen.UsersModelImage(manage_user_id, language),
        )
        logger.info(f"Opened the user #{manage_user_id} image model menu for user #{user_id}")
        return user_info
    elif len(data) == 5:
        image_model = data[3].lower()
        if SetUserImageModel(manage_user_id, image_model):
            bot.answer_callback_query(
                callback_query_id=call_id,
                text=f"{Translate(language, 'manage_model_image_success')}{manage_user_info['user_name']} {Translate(language, 'manage_settings_success')} {image_model}",
                show_alert=True,
            )
            if image_model != manage_user_info['image_model']:
                bot.edit_message_text(
                    text=f"{Translate(language, 'manage_model_image')}{manage_user_info['user_name']}? ({Translate(language, 'current_value')} {image_model})",
                    chat_id=user_info['chat_id'],
                    message_id=message_id,
                    reply_markup=kb_gen.UsersModelImage(manage_user_id, language),
                )
            logger.info(f"Successfully changed the user #{manage_user_id} image model to '{image_model}' by user #{user_id}")
            return user_info
    
    HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
    return user_info

# Handle callback query for managing the user's translate model
def HandleManageTranslateModelCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo, manage_user_id: int, manage_user_info: UserInfo) -> UserInfo:
    language = user_info['bot_language']

    if len(data) == 4:
        bot.edit_message_text(
            text=f"{Translate(language, 'manage_model_translate')}{manage_user_info['user_name']}? ({Translate(language, 'current_value')} {manage_user_info['translate_model']})",
            chat_id=user_info['chat_id'],
            message_id=message_id,
            reply_markup=kb_gen.UsersModelTranslate(manage_user_id, language),
        )
        logger.info(f"Opened the user #{manage_user_id} audio translate model menu for user #{user_id}")
        return user_info
    elif len(data) == 5:
        translate_model = data[3].lower()
        if SetUserTranslateModel(manage_user_id, translate_model):
            bot.answer_callback_query(
                callback_query_id=call_id,
                text=f"{Translate(language, 'manage_model_translate_success')}{manage_user_info['user_name']} {Translate(language, 'manage_settings_success')} {translate_model}",
                show_alert=True,
            )
            if translate_model != manage_user_info['translate_model']:
                bot.edit_message_text(
                    text=f"{Translate(language, 'manage_model_translate')}{manage_user_info['user_name']}? ({Translate(language, 'current_value')} {translate_model})",
                    chat_id=user_info['chat_id'],
                    message_id=message_id,
                    reply_markup=kb_gen.UsersModelTranslate(manage_user_id, language),
                )
            logger.info(f"Successfully changed the user #{manage_user_id} audio translate model to '{translate_model}' by user #{user_id}")
            return user_info
    
    HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
    return user_info

# Handle callback query for managing the user's STT model
def HandleManageSTTModelCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo, manage_user_id: int, manage_user_info: UserInfo) -> UserInfo:
    language = user_info['bot_language']

    if len(data) == 4:
        bot.edit_message_text(
            text=f"{Translate(language, 'manage_model_transcribe')}{manage_user_info['user_name']}? ({Translate(language, 'current_value')} {manage_user_info['stt_model']})",
            chat_id=user_info['chat_id'],
            message_id=message_id,
            reply_markup=kb_gen.UsersModelTranscribe(manage_user_id, language),
        )
        logger.info(f"Opened the user #{manage_user_id} audio transcribe model menu for user #{user_id}")
        return user_info
    elif len(data) == 5:
        stt_model = data[3].lower()
        if SetUserSTTModel(manage_user_id, stt_model):
            bot.answer_callback_query(
                callback_query_id=call_id,
                text=f"{Translate(language, 'manage_model_transcribe_success')}{manage_user_info['user_name']} {Translate(language, 'manage_settings_success')} {stt_model}",
                show_alert=True,
            )
            if stt_model != manage_user_info['stt_model']:
                bot.edit_message_text(
                    text=f"{Translate(language, 'manage_model_transcribe')}{manage_user_info['user_name']}? ({Translate(language, 'current_value')} {stt_model})",
                    chat_id=user_info['chat_id'],
                    message_id=message_id,
                    reply_markup=kb_gen.UsersModelTranscribe(manage_user_id, language),
                )
            logger.info(f"Successfully changed the user #{manage_user_id} audio transcribe model to '{stt_model}' by user #{user_id}")
            return user_info
    
    HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
    return user_info

# Handle callback query for managing the user's TTS model
def HandleManageTTSModelCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo, manage_user_id: int, manage_user_info: UserInfo) -> UserInfo:
    language = user_info['bot_language']

    if len(data) == 4:
        bot.edit_message_text(
            text=f"{Translate(language, 'manage_model_syntesize')}{manage_user_info['user_name']}? ({Translate(language, 'current_value')} {manage_user_info['tts_model']})",
            chat_id=user_info['chat_id'],
            message_id=message_id,
            reply_markup=kb_gen.UsersModelSyntesize(manage_user_id, language),
        )
        logger.info(f"Opened the user #{manage_user_id} audio syntesize model menu for user #{user_id}")
        return user_info
    elif len(data) == 5:
        tts_model = data[3].lower()
        if SetUserTTSModel(manage_user_id, tts_model):
            bot.answer_callback_query(
                callback_query_id=call_id,
                text=f"{Translate(language, 'manage_model_syntesize_success')}{manage_user_info['user_name']} {Translate(language, 'manage_settings_success')} {tts_model}",
                show_alert=True,
            )
            if tts_model != manage_user_info['tts_model']:
                bot.edit_message_text(
                    text=f"{Translate(language, 'manage_model_syntesize')}{manage_user_info['user_name']}? ({Translate(language, 'current_value')} {tts_model})",
                    chat_id=user_info['chat_id'],
                    message_id=message_id,
                    reply_markup=kb_gen.UsersModelSyntesize(manage_user_id, language),
                )
            logger.info(f"Successfully changed the user #{manage_user_id} audio syntesize model to '{tts_model}' by user #{user_id}")
            return user_info
    
    HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
    return user_info


# Handle callback query for managing the user's chat model temperature
def HandleManageTemperatureCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo, manage_user_id: int, manage_user_info: UserInfo) -> UserInfo:
    language = user_info['bot_language']

    if len(data) == 3:
        bot.edit_message_text(
            text=f"{Translate(language, 'manage_temperature')}{manage_user_info['user_name']}? ({Translate(language, 'current_value')} {manage_user_info['temperature']})",
            chat_id=user_info['chat_id'],
            message_id=message_id,
            reply_markup=kb_gen.UsersTemperature(manage_user_id, language),
        )
        logger.info(f"Opened the user #{manage_user_id} temperature menu for user #{user_id}")
        return user_info
    elif len(data) == 4:
        temperature = data[2].lower()
        if SetUserTemperature(manage_user_id, temperature):
            bot.answer_callback_query(
                callback_query_id=call_id,
                text=f"{Translate(language, 'manage_temperature_success')}{manage_user_info['user_name']} {Translate(language, 'manage_settings_success')} {temperature}",
                show_alert=True,
            )
            if temperature != str(manage_user_info['temperature']):
                bot.edit_message_text(
                    text=f"{Translate(language, 'manage_temperature')}{manage_user_info['user_name']}? ({Translate(language, 'current_value')} {temperature})",
                    chat_id=user_info['chat_id'],
                    message_id=message_id,
                    reply_markup=kb_gen.UsersTemperature(manage_user_id, language),
                )
            logger.info(f"Successfully changed the user #{manage_user_id} temperature to '{temperature}' by user #{user_id}")
            return user_info

    HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
    return user_info

# Handle callback query for managing the user's chat model token limit
def HandleManageTokenLimitCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo, manage_user_id: int, manage_user_info: UserInfo) -> UserInfo:
    language = user_info['bot_language']

    if len(data) == 4 and data[2].lower() == 'limit':
        bot.edit_message_text(
            text=f"{Translate(language, 'manage_token_limit')}{manage_user_info['user_name']}? ({Translate(language, 'current_value')} {manage_user_info['token_limit']})",
            chat_id=user_info['chat_id'],
            message_id=message_id,
            reply_markup=kb_gen.UsersTokenLimit(manage_user_id, language),
        )
        logger.info(f"Opened the user #{manage_user_id} token limit menu for user #{user_id}")
        return user_info
    elif len(data) == 5:
        token_limit = data[3].lower()
        if SetUserTokenLimit(manage_user_id, token_limit):
            bot.answer_callback_query(
                callback_query_id=call_id,
                text=f"{Translate(language, 'manage_token_limit_success')}{manage_user_info['user_name']} {Translate(language, 'manage_settings_success')} {token_limit}",
                show_alert=True,
            )
            if token_limit != str(manage_user_info['token_limit']):
                bot.edit_message_text(
                    text=f"{Translate(language, 'manage_token_limit')}{manage_user_info['user_name']}? ({Translate(language, 'current_value')} {token_limit})",
                    chat_id=user_info['chat_id'],
                    message_id=message_id,
                    reply_markup=kb_gen.UsersTokenLimit(manage_user_id, language),
                )
            logger.info(f"Successfully changed the user #{manage_user_id} token limit to '{token_limit}' by user #{user_id}")
            return user_info

    HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
    return user_info

# Handle callback query for managing the user's budget
def HandleManageBudgetCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo, manage_user_id: int, manage_user_info: UserInfo) -> UserInfo:
    language = user_info['bot_language']

    if len(data) == 3:
        bot.edit_message_text(
            text=f"{Translate(language, f"manage_{manage_user_info['user_role']}_budget")}{manage_user_info['user_name']}? ({Translate(language, 'current_value')} {manage_user_info['user_budget']}$)",
            chat_id=user_info['chat_id'],
            message_id=message_id,
            reply_markup=kb_gen.UsersBudget(manage_user_id, language),
        )
        logger.info(f"Opened the user #{manage_user_id} budget menu for user #{user_id}")
        return user_info
    elif len(data) == 4:
        action = data[2].lower()
        if action == 'increase':
            budget = manage_user_info['user_budget'] + Decimal('0.1')
            bot.answer_callback_query(
                callback_query_id=call_id,
                text=f"{Translate(language, f"manage_{manage_user_info['user_role']}_budget_changed")}{manage_user_info['user_name']} {Translate(language, 'manage_budget_increased')} {budget}$",
                show_alert=True,
            )
            logger.info(f"Successfully increased the user #{manage_user_id} budget by 0.1$ by user #{user_id}")
        elif action == 'decrease' and manage_user_info['user_budget'] > Decimal('0.1'):
            budget = manage_user_info['user_budget'] - Decimal('0.1')
            bot.answer_callback_query(
                callback_query_id=call_id,
                text=f"{Translate(language, f"manage_{manage_user_info['user_role']}_budget_changed")}{manage_user_info['user_name']} {Translate(language, 'manage_budget_decreased')} {budget}$",
                show_alert=True,
            )
            logger.info(f"Successfully decreased the user #{manage_user_id} budget by 0.1$ by user #{user_id}")
        elif action == 'decrease':
            budget = Decimal('0')
            bot.answer_callback_query(
                callback_query_id=call_id,
                text=f"{Translate(language, f"manage_{manage_user_info['user_role']}_budget_changed")}{manage_user_info['user_name']} {Translate(language, 'manage_budget_zero')}",
                show_alert=True,
            )
            logger.info(f"Successfully set the user #{manage_user_id} budget to 0$ by user #{user_id}")
        else:
            HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
            return user_info
        
        SetUserBudget(manage_user_id, budget)
        if budget != manage_user_info['user_budget']:
            bot.edit_message_text(
                text=f"{Translate(language, f"manage_{manage_user_info['user_role']}_budget")}{manage_user_info['user_name']}? ({Translate(language, 'current_value')} {budget}$)",
                chat_id=user_info['chat_id'],
                message_id=message_id,
                reply_markup=kb_gen.UsersBudget(manage_user_id, language),
            )
        return user_info

    HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
    return user_info

# Handle callback query for managing the user's deletion
def HandleManageDeleteCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo, manage_user_id: int, manage_user_info: UserInfo) -> UserInfo:
    language = user_info['bot_language']

    if len(data) == 3:
        bot.edit_message_text(
            text=f"{Translate(language, f"manage_{manage_user_info['user_role']}_delete")}{manage_user_info['user_name']} {Translate(language, 'manage_delete_end')}",
            chat_id=user_info['chat_id'],
            message_id=message_id,
            reply_markup=kb_gen.UsersDelete(manage_user_id, language),
        )
        logger.warning(f"User #{user_id} asked for deletion of user #{manage_user_id} from the database")
        return user_info
    
    HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
    return user_info

# Handle callback query for managing the user's removal
def HandleManageRemoveCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo, manage_user_id: int, manage_user_info: UserInfo) -> UserInfo:
    language = user_info['bot_language']

    if len(data) == 3:
        DeleteUser(manage_user_id)
        bot.answer_callback_query(
            callback_query_id=call_id,
            text=f"@{manage_user_info['user_name']} {Translate(language, 'manage_delete_success')}",
            show_alert=True,
        )
        logger.warning(f"User #{user_id} deleted user #{manage_user_id} from the database")
        match manage_user_info['user_role']:
            case 'admin':
                return HandleUserCategotiesCallbackQuery(bot, call_id, message_id, user_id, user_info, 'admins')
            case 'user':
                return HandleUserCategotiesCallbackQuery(bot, call_id, message_id, user_id, user_info, 'users')
            case 'banned':
                return HandleUserCategotiesCallbackQuery(bot, call_id, message_id, user_id, user_info, 'banned')
            case _:
                HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
                return user_info
    
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