from decimal import Decimal
from logging import Logger
from telebot import TeleBot
from telebot.types import Message, ReplyParameters

import utils.openai.helper
from utils.users import UserInfo
from utils.translations import GetTranslation as Translate
from utils.yandexcloud.user_management import SetUserBudget

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
            chat_model = user_info['chat_model']

            # Call the OpenAI API through the OpenAIHelper
            response, usage = utils.openai.helper.GetTextResponse(
                user_id=user_id,
                message=user_message,
                chat_model=chat_model,
            )

            # Calculate the cost of the response and change the budget
            cost = utils.openai.helper.CalculateTextCost(usage, chat_model)
            budget_exceeded = cost > budget
            user_info['user_budget'] = budget - cost
            SetUserBudget(user_id, user_info['user_budget'])

            # Send the response back to the user
            bot.send_message(
                chat_id=user_info['chat_id'],
                reply_parameters=ReplyParameters(message_id=message.message_id),
                text=response,
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