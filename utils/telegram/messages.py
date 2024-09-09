from decimal import Decimal
from logging import Logger
from telebot import TeleBot
from telebot.types import Message, ReplyParameters
from telebot.util import smart_split, antiflood

import utils.openai.helper
from utils.users import UserInfo
from utils.translations import GetTranslation as Translate

# Define logger
logger: Logger

# Handle text messages
def HandleTextMessage(bot: TeleBot, message: Message, user_info: UserInfo):
    user_id = message.from_user.id
    user_message = message.text

    logger.info(f"Received text message from user #{user_id}: {len(user_message)} characters long")

    budget = user_info['user_budget']
    budget_exceeded = budget <= Decimal(0)
    if not budget_exceeded:
        try:
            bot.send_chat_action(message.chat.id, 'typing')

            chat_model = user_info['chat_model']

            # Call the OpenAI API through the OpenAIHelper
            response = utils.openai.helper.GetTextResponse(
                user_id=user_id,
                chat_id=user_info['chat_id'],
                request=user_message,
                chat_model=chat_model,
                temperature=user_info['temperature'],
                max_tokens=user_info['token_limit'],
                budget=user_info['user_budget'],
            )

            # Send the response back to the user
            sent_message = message
            for chunk in smart_split(response):
                sent_message = antiflood(
                    bot.send_message,
                    chat_id=user_info['chat_id'],
                    reply_parameters=ReplyParameters(message_id=sent_message.message_id),
                    text=chunk,
                    parse_mode='Markdown',
                )

            logger.info(f"Sent text response to user #{user_id}: {len(response)} characters long")

        except Exception as e:
            bot.send_message(
                chat_id=user_info['chat_id'],
                reply_parameters=ReplyParameters(message_id=message.message_id),
                text=Translate(user_info['bot_language'], 'error_processing_message'),
            )

            logger.error(f"Error processing text message for user #{user_id}: {str(e)}", exc_info=True)

    # Send a message to the user if he has exceeded his budget
    if budget_exceeded:
        bot.send_message(
            chat_id=message.chat.id,
            text=Translate(user_info['bot_language'], 'warning_budget_exceeded'),
        )

        logger.warning(f"User #{user_id} has exceeded his budget")

# Handle photo messages
def HandlePhotoMessage(bot: TeleBot, message: Message, user_info: UserInfo):
    logger.info(f"Received photo message from user #{message.from_user.id}")

    bot.send_message(
        chat_id=user_info['chat_id'],
        reply_parameters=ReplyParameters(message_id=message.message_id),
        text="This type of message is not supported yet",
    )

# Handle audio messages
def HandleAudioMessage(bot: TeleBot, message: Message, user_info: UserInfo):
    logger.info(f"Received audio message from user #{message.from_user.id}")

    bot.send_message(
        chat_id=user_info['chat_id'],
        reply_parameters=ReplyParameters(message_id=message.message_id),
        text="This type of message is not supported yet",
    )

# Handle voice messages
def HandleVoiceMessage(bot: TeleBot, message: Message, user_info: UserInfo):
    logger.info(f"Received voice message from user #{message.from_user.id}")
    
    bot.send_message(
        chat_id=user_info['chat_id'],
        reply_parameters=ReplyParameters(message_id=message.message_id),
        text="This type of message is not supported yet",
    )

# Handle video messages
def HandleVideoMessage(bot: TeleBot, message: Message, user_info: UserInfo):
    logger.info(f"Received video message from user #{message.from_user.id}")

    bot.send_message(
        chat_id=user_info['chat_id'],
        reply_parameters=ReplyParameters(message_id=message.message_id),
        text="This type of message is not supported yet",
    )

# Handle video note messages
def HandleVideoNoteMessage(bot: TeleBot, message: Message, user_info: UserInfo):
    logger.info(f"Received video note message from user #{message.from_user.id}")

    bot.send_message(
        chat_id=user_info['chat_id'],
        reply_parameters=ReplyParameters(message_id=message.message_id),
        text="This type of message is not supported yet",
    )

# Handle document messages
def HandleDocumentMessage(bot: TeleBot, message: Message, user_info: UserInfo):
    logger.info(f"Received document message from user #{message.from_user.id}")

    bot.send_message(
        chat_id=user_info['chat_id'],
        reply_parameters=ReplyParameters(message_id=message.message_id),
        text="This type of message is not supported yet",
    )

# Handle dice messages
def HandleDiceMessage(bot: TeleBot, message: Message, user_info: UserInfo):
    logger.info(f"Received dice message from user #{message.from_user.id}")

    bot.send_message(
        chat_id=user_info['chat_id'],
        reply_parameters=ReplyParameters(message_id=message.message_id),
        text="This type of message is not supported yet",
    )

# Handle messages of unsupported types
def HandleUnknownMessage(bot: TeleBot, message: Message, language: str):
    bot.send_message(
        chat_id=message.chat.id,
        text=Translate(language, 'warning_message_unknown'),
        reply_parameters=ReplyParameters(message_id=message.message_id),
    )

    logger.warning(f"Message of unsupported type '{message.content_type}' received from user #{message.from_user.id}")

# Send a message to the user if he is not allowed to send messages to the bot
def HandleDisallowedMessage(bot: TeleBot, message: Message, user_info: UserInfo):
    bot.send_message(
        chat_id=message.chat.id,
        text=Translate(user_info['bot_language'], 'warning_message_disallowed'),
        reply_parameters=ReplyParameters(message_id=message.message_id),
    )

    logger.warning(f"User #{message.from_user.id} is not allowed to send messages to the bot")