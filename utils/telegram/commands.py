from decimal import Decimal
from logging import Logger
from telebot import TeleBot
from telebot.types import BotCommand, BotCommandScopeChat, Message, ReplyParameters

import utils.openai.helper
import utils.telegram.keyboards as kb_gen
from utils.translations import GetTranslation as Translate

# Define logger
logger: Logger

# Define base commands for the bot
def GetBaseCommands(language: str = 'en') -> list[BotCommand]:
    return [
        BotCommand('start', Translate(language, 'command_description_start')),
        BotCommand('help', Translate(language, 'command_description_help')),
        BotCommand('language', Translate(language, 'command_description_language')),
        BotCommand('budget', Translate(language, 'command_description_budget')),
    ]

# Define the commands for the users of the bot
def GetUserCommands(language: str = 'en') -> list[BotCommand]:
    return GetBaseCommands(language) + [
        BotCommand('reset', Translate(language, 'command_description_reset')),
        BotCommand('summarize', Translate(language, 'command_description_summarize')),
    ]

# Define the commands for the admins of the bot
def GetAdminCommands(language: str = 'en') -> list[BotCommand]:
    return GetUserCommands(language) + [
        BotCommand('settings', Translate(language, 'command_description_settings')),
    ]

# Define the commands for the owner of the bot
def GetOwnerCommands(language: str = 'en') -> list[BotCommand]:
    return GetAdminCommands(language) + [
        BotCommand('users', Translate(language, 'command_description_users')),
    ]

# Update the bot's commands for the specified user
def UpdateBotCommands(bot: TeleBot, chat_id: int | str, user_role: str = 'banned', language: str = 'en'):
    match user_role:
        case 'owner':
            commands = GetOwnerCommands(language)
        case 'admin':
            commands = GetAdminCommands(language)
        case 'user':
            commands = GetUserCommands(language)
        case _:
            commands = GetBaseCommands(language)

    bot.set_my_commands(scope=BotCommandScopeChat(int(chat_id)), commands=commands)


# Send a start message to the user
def Start(bot: TeleBot, chat_id: int, language: str):
    bot.send_message(
        chat_id=chat_id,
        text=Translate(language, 'command_message_start'),
    )

# Send a help message to the user
def Help(bot: TeleBot, chat_id: int, language: str, user_role: str):
    help_message = Translate(language, 'command_message_help_start')

    help_message += f"/start - {Translate(language, 'command_description_start')}\n"
    help_message += f"/help - {Translate(language, 'command_description_help')}\n"
    help_message += f"/language - {Translate(language, 'command_description_language')}\n"
    help_message += f"/budget - {Translate(language, 'command_description_budget')}\n"

    if user_role in ('owner', 'admin', 'user', ):
        help_message += f"/reset - {Translate(language, 'command_description_reset')}\n"
        help_message += f"/summarize - {Translate(language, 'command_description_summarize')}\n"

    if user_role in ('owner', 'admin', ):
        help_message += f"/settings - {Translate(language, 'command_description_settings')}\n"

    if user_role in ('owner', ):
        help_message += f"/users - {Translate(language, 'command_description_users')}\n"

    help_message += Translate(language, 'command_message_help_end')

    bot.send_message(
        chat_id=chat_id,
        text=help_message,
    )

# Change the bot's language for the user
def Language(bot: TeleBot, chat_id: int, language: str):
    bot.send_message(
        chat_id=chat_id,
        text=f"{Translate(language, 'command_message_language')} ({Translate(language, 'current_value')} {Translate(language, 'language')})",
        reply_markup=kb_gen.Language(),
    )

# Get the bot's budget for the user
def Budget(bot: TeleBot, chat_id: int, language: str, budget: Decimal):
    bot.send_message(
        chat_id=chat_id,
        text=f"{Translate(language, 'command_message_budget')} {budget}$",
    )

# Reset the conversation history
def Reset(bot: TeleBot, chat_id: int, language: str):
    bot.send_message(
        chat_id=chat_id,
        text=Translate(language, 'command_message_reset'),
        reply_markup=kb_gen.Reset(language),
    )

# Summarize the conversation
def Summarize(bot: TeleBot, user_id: int, chat_id: int, language: str):
    utils.openai.helper.SummarizeConversation(user_id)

    bot.send_message(
        chat_id=chat_id,
        text=Translate(language, 'command_message_summarize'),
    )

    logger.info(f"Successfully summarized conversation history for user #{user_id}")

# Get the bot's settings
def Settings(bot: TeleBot, chat_id: int, language: str):
    bot.send_message(
        chat_id=chat_id,
        text=Translate(language, 'command_message_settings'),
        reply_markup=kb_gen.Settings(language),
    )

# Manage users and admins of the bot
def Users(bot: TeleBot, chat_id: int, language: str):
    bot.send_message(
        chat_id=chat_id,
        text=Translate(language, 'command_message_users'),
        reply_markup=kb_gen.Users(language),
    )

# Handle any unknown command
def HandleUnknownCommand(bot: TeleBot, message: Message, language: str):
    bot.send_message(
        chat_id=message.chat.id,
        text=Translate(language, 'warning_command_unknown'),
        reply_parameters=ReplyParameters(message_id=message.message_id),
    )

    logger.warning(f"Unrecognized command '{message.text}' received from user #{message.from_user.id}")

# Send a message to the user if he is not allowed to send the command
def HandleDisallowedCommand(bot: TeleBot, message: Message, language: str):
    bot.send_message(
        chat_id=message.chat.id,
        text=Translate(language, 'warning_command_disallowed'),
        reply_parameters=ReplyParameters(message_id=message.message_id),
    )
    
    logger.warning(f"User #{message.from_user.id} is not allowed to send the command '{message.text}'")