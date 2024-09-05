from logging import Logger
from telebot import TeleBot

import utils.telegram.keyboards as kb_gen
from utils.users import UserInfo
from utils.translations import GetTranslation as Translate
from utils.yandexcloud.user_management import (
    SetUserChatModel, SetUserVisionModel, SetUserImageModel,
    SetUserTranslateModel, SetUserSTTModel, SetUserTTSModel,
    SetUserTemperature, SetUserTokenLimit,
)

# Define services
logger: Logger

# Handle settings model chat callback query
def HandleModelChatCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo) -> UserInfo:
    language = user_info['bot_language']

    if len(data) == 3:
        bot.edit_message_text(
            text=f"{Translate(language, 'choice_model_chat')} ({Translate(language, 'current_value')} {user_info['chat_model']})",
            chat_id=user_info['chat_id'],
            message_id=message_id,
            reply_markup=kb_gen.SettingsModelChat(language),
        )
        logger.info(f"Opened the chat model menu for user #{user_id}")
        return user_info
    
    if len(data) != 4:
        HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
        return user_info
    
    model = data[3].lower()
    if model == user_info['chat_model']:
        bot.answer_callback_query(
            callback_query_id=call_id,
            text=Translate(language, 'warning_same_model'),
            show_alert=True,
        )
        logger.info(f"User #{user_id} tried to set the chat model to the same model as the current one ('{model}')")
        return user_info

    if not SetUserChatModel(user_id, model):
        HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
        return user_info

    user_info['chat_model'] = model

    bot.send_message(
        chat_id=user_info['chat_id'],
        text=f"{Translate(language, 'success_changed_model_chat')} {model}",
    )

    bot.edit_message_text(
        text=f"{Translate(language, 'choice_model_chat')} ({Translate(language, 'current_value')} {user_info['chat_model']})",
        chat_id=user_info['chat_id'],
        message_id=message_id,
        reply_markup=kb_gen.SettingsModelChat(language),
    )

    logger.info(f"Successfully changed the chat model for user #{user_id} to '{model}'")

    return user_info

# Handle settings model vision callback query
def HandleModelVisionCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo) -> UserInfo:
    language = user_info['bot_language']

    if len(data) == 3:
        bot.edit_message_text(
            text=f"{Translate(language, 'choice_model_vision')} ({Translate(language, 'current_value')} {user_info['vision_model']})",
            chat_id=user_info['chat_id'],
            message_id=message_id,
            reply_markup=kb_gen.SettingsModelVision(language),
        )
        logger.info(f"Opened the vision model menu for user #{user_id}")
        return user_info

    if len(data) != 4:
        HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
        return user_info
    
    model = data[3].lower()
    if model == user_info['vision_model']:
        bot.answer_callback_query(
            callback_query_id=call_id,
            text=Translate(language, 'warning_same_model'),
            show_alert=True,
        )
        logger.info(f"User #{user_id} tried to set the vision model to the same model as the current one ('{model}')")
        return user_info

    if not SetUserVisionModel(user_id, model):
        HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
        return user_info
    
    user_info['vision_model'] = model

    bot.send_message(
        chat_id=user_info['chat_id'],
        text=f"{Translate(language, 'success_changed_model_vision')} {model}",
    )

    bot.edit_message_text(
        text=f"{Translate(language, 'choice_model_vision')} ({Translate(language, 'current_value')} {user_info['vision_model']})",
        chat_id=user_info['chat_id'],
        message_id=message_id,
        reply_markup=kb_gen.SettingsModelVision(language),
    )

    logger.info(f"Successfully changed the vision model for user #{user_id} to '{model}'")

    return user_info

# Handle settings model image callback query
def HandleModelImageCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo) -> UserInfo:
    language = user_info['bot_language']

    if len(data) == 3:
        bot.edit_message_text(
            text=f"{Translate(language, 'choice_model_image')} ({Translate(language, 'current_value')} {user_info['image_model']})",
            chat_id=user_info['chat_id'],
            message_id=message_id,
            reply_markup=kb_gen.SettingsModelImage(language),
        )
        logger.info(f"Opened the image model menu for user #{user_id}")
        return user_info

    if len(data) != 4:
        HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
        return user_info
    
    model = data[3].lower()
    if model == user_info['image_model']:
        bot.answer_callback_query(
            callback_query_id=call_id,
            text=Translate(language, 'warning_same_model'),
            show_alert=True,
        )
        logger.info(f"User #{user_id} tried to set the image model to the same model as the current one ('{model}')")
        return user_info

    if not SetUserImageModel(user_id, model):
        HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
        return user_info
    
    user_info['image_model'] = model

    bot.send_message(
        chat_id=user_info['chat_id'],
        text=f"{Translate(language, 'success_changed_model_image')} {model}",
    )

    bot.edit_message_text(
        text=f"{Translate(language, 'choice_model_image')} ({Translate(language, 'current_value')} {user_info['image_model']})",
        chat_id=user_info['chat_id'],
        message_id=message_id,
        reply_markup=kb_gen.SettingsModelImage(language),
    )

    logger.info(f"Successfully changed the image model for user #{user_id} to '{model}'")

    return user_info

# Handle settings model translate callback query
def HandleModelTranslateCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo) -> UserInfo:
    language = user_info['bot_language']

    if len(data) == 3:
        bot.edit_message_text(
            text=f"{Translate(language, 'choice_model_translate')} ({Translate(language, 'current_value')} {user_info['translate_model']})",
            chat_id=user_info['chat_id'],
            message_id=message_id,
            reply_markup=kb_gen.SettingsModelTranslate(language),
        )
        logger.info(f"Opened the audio translate model menu for user #{user_id}")
        return user_info

    if len(data) != 4:
        HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
        return user_info
    
    model = data[3].lower()
    if model == user_info['translate_model']:
        bot.answer_callback_query(
            callback_query_id=call_id,
            text=Translate(language, 'warning_same_model'),
            show_alert=True,
        )
        logger.info(f"User #{user_id} tried to set the audio translate model to the same model as the current one ('{model}')")
        return user_info

    if not SetUserTranslateModel(user_id, model):
        HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
        return user_info
    
    user_info['translate_model'] = model

    bot.send_message(
        chat_id=user_info['chat_id'],
        text=f"{Translate(language, 'success_changed_model_translate')} {model}",
    )

    logger.info(f"Successfully changed the audio translate model for user #{user_id} to '{model}'")

    return user_info

# Handle settings model transcribe callback query
def HandleModelTranscribeCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo) -> UserInfo:
    language = user_info['bot_language']

    if len(data) == 3:
        bot.edit_message_text(
            text=f"{Translate(language, 'choice_model_transcribe')} ({Translate(language, 'current_value')} {user_info['stt_model']})",
            chat_id=user_info['chat_id'],
            message_id=message_id,
            reply_markup=kb_gen.SettingsModelTranscribe(language),
        )
        logger.info(f"Opened the audio transcribe model menu for user #{user_id}")
        return user_info

    if len(data) != 4:
        HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
        return user_info
    
    model = data[3].lower()
    if model == user_info['stt_model']:
        bot.answer_callback_query(
            callback_query_id=call_id,
            text=Translate(language, 'warning_same_model'),
            show_alert=True,
        )
        logger.info(f"User #{user_id} tried to set the audio transcribe model to the same model as the current one ('{model}')")
        return user_info

    if not SetUserSTTModel(user_id, model):
        HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
        return user_info
    
    user_info['stt_model'] = model

    bot.send_message(
        chat_id=user_info['chat_id'],
        text=f"{Translate(language, 'success_changed_model_transcribe')} {model}",
    )

    bot.edit_message_text(
        text=f"{Translate(language, 'choice_model_transcribe')} ({Translate(language, 'current_value')} {user_info['stt_model']})",
        chat_id=user_info['chat_id'],
        message_id=message_id,
        reply_markup=kb_gen.SettingsModelTranscribe(language),
    )

    logger.info(f"Successfully changed the audio transcribe model for user #{user_id} to '{model}'")

    return user_info

# Handle settings model syntesize callback query
def HandleModelSyntesizeCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo) -> UserInfo:
    language = user_info['bot_language']

    if len(data) == 3:
        bot.edit_message_text(
            text=f"{Translate(language, 'choice_model_syntesize')} ({Translate(language, 'current_value')} {user_info['tts_model']})",
            chat_id=user_info['chat_id'],
            message_id=message_id,
            reply_markup=kb_gen.SettingsModelSyntesize(language),
        )
        logger.info(f"Opened the audio syntesize model menu for user #{user_id}")
        return user_info

    if len(data) != 4:
        HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
        return user_info
    
    model = data[3].lower()
    if model == user_info['tts_model']:
        bot.answer_callback_query(
            callback_query_id=call_id,
            text=Translate(language, 'warning_same_model'),
            show_alert=True,
        )
        logger.info(f"User #{user_id} tried to set the audio syntesize model to the same model as the current one ('{model}')")
        return user_info

    if not SetUserTTSModel(user_id, model):
        HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
        return user_info
    
    user_info['tts_model'] = model

    bot.send_message(
        chat_id=user_info['chat_id'],
        text=f"{Translate(language, 'success_changed_model_syntesize')} {model}",
    )

    bot.edit_message_text(
        text=f"{Translate(language, 'choice_model_syntesize')} ({Translate(language, 'current_value')} {user_info['tts_model']})",
        chat_id=user_info['chat_id'],
        message_id=message_id,
        reply_markup=kb_gen.SettingsModelSyntesize(language),
    )

    logger.info(f"Successfully changed the audio syntesize model for user #{user_id} to '{model}'")

    return user_info

# Handle settings temperature callback query
def HandleTemperatureCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo) -> UserInfo:
    language = user_info['bot_language']

    if len(data) == 2:
        bot.edit_message_text(
            text=f"{Translate(language, 'choice_temperature')} ({Translate(language, 'current_value')} {user_info['temperature']})",
            chat_id=user_info['chat_id'],
            message_id=message_id,
            reply_markup=kb_gen.SettingsTemperature(language),
        )
        logger.info(f"Opened the temperature menu for user #{user_id}")
        return user_info

    if len(data) != 3:
        HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
        return user_info
    
    temperature = data[2].lower()
    if temperature == str(user_info['temperature']):
        bot.answer_callback_query(
            callback_query_id=call_id,
            text=Translate(language, 'warning_same_temperature'),
            show_alert=True,
        )
        logger.info(f"User #{user_id} tried to set the temperature to the same temperature as the current one ('{temperature}')")
        return user_info

    if not SetUserTemperature(user_id, temperature):
        HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
        return user_info
    
    user_info['temperature'] = temperature

    bot.send_message(
        chat_id=user_info['chat_id'],
        text=f"{Translate(language, 'success_changed_temperature')} {temperature}",
    )

    bot.edit_message_text(
        text=f"{Translate(language, 'choice_temperature')} ({Translate(language, 'current_value')} {user_info['temperature']})",
        chat_id=user_info['chat_id'],
        message_id=message_id,
        reply_markup=kb_gen.SettingsTemperature(language),
    )

    logger.info(f"Successfully changed the temperature for user #{user_id} to '{temperature}'")

    return user_info

# Handle settings token limit callback query
def HandleTokenLimitCallbackQuery(bot: TeleBot, call_id: int, data: list[str], message_id: int, user_id: int, user_info: UserInfo) -> UserInfo:
    language = user_info['bot_language']

    if len(data) == 3:
        bot.edit_message_text(
            text=f"{Translate(language, 'choice_token_limit')} ({Translate(language, 'current_value')} {user_info['token_limit']})",
            chat_id=user_info['chat_id'],
            message_id=message_id,
            reply_markup=kb_gen.SettingsTokenLimit(language),
        )
        logger.info(f"Opened the token limit menu for user #{user_id}")
        return user_info

    if len(data) != 4:
        HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
        return user_info
    
    token_limit = data[3].lower()
    if token_limit == str(user_info['token_limit']):
        bot.answer_callback_query(
            callback_query_id=call_id,
            text=Translate(language, 'warning_same_token_limit'),
            show_alert=True,
        )
        logger.info(f"User #{user_id} tried to set the token limit to the same token limit as the current one ('{token_limit}')")
        return user_info

    if not SetUserTokenLimit(user_id, token_limit):
        HandleUnknownCallbackQuery(bot, call_id, data, user_id, user_info)
        return user_info
    
    user_info['token_limit'] = token_limit

    bot.send_message(
        chat_id=user_info['chat_id'],
        text=f"{Translate(language, 'success_changed_token_limit')} {token_limit}",
    )

    bot.edit_message_text(
        text=f"{Translate(language, 'choice_token_limit')} ({Translate(language, 'current_value')} {user_info['token_limit']})",
        chat_id=user_info['chat_id'],
        message_id=message_id,
        reply_markup=kb_gen.SettingsTokenLimit(language),
    )

    logger.info(f"Successfully changed the token limit for user #{user_id} to '{token_limit}'")

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