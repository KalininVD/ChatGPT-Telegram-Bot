# Import the necessary modules
from telebot import TeleBot
from telebot.types import BotCommand, BotCommandScopeChat
from boto3 import Session
from botocore.exceptions import ClientError
import yandexcloud
from yandex.cloud.lockbox.v1.payload_service_pb2 import GetPayloadRequest
from yandex.cloud.lockbox.v1.payload_service_pb2_grpc import PayloadServiceStub
from decimal import Decimal

# Environment variables
SECRET_ID: str | None = None
DOCAPI_ENDPOINT: str | None = None

# Service variables
boto_session = None
docapi_table = None

# Define the base commands for the bot
BASE_COMMANDS = [
    BotCommand('start', 'Get started with ChatGPT Telegram Bot'),
    BotCommand('help', 'Get help message of the bot'),
    BotCommand('change_language', 'Change the language for the bot'),
]

# Define the commands for the users of the bot
USER_COMMANDS = BASE_COMMANDS + [
    BotCommand('stats', 'Get the statistics of the bot usage'),
    BotCommand('reset', 'Start a new conversation'),
    BotCommand('summarize', 'Summarize the last conversation'),
]

# Define the commands for the admins of the bot
ADMIN_COMMANDS = USER_COMMANDS + [
    BotCommand('settings', 'Get the bot settings'),
    BotCommand('change_model', 'Change the model for the bot'),
]

# Define the commands for the owner of the bot
OWNER_COMMANDS = ADMIN_COMMANDS + [
    BotCommand('users', 'Manage users and admins of the bot'),
]

# Update the bot's commands for the user
def UpdateBotCommands(telegram_bot: TeleBot, chat_id: int, user_id: int):
    match GetUserCategory(user_id):
        case 'owner':
            telegram_bot.set_my_commands(scope=BotCommandScopeChat(chat_id), commands=OWNER_COMMANDS)
        case 'admin':
            telegram_bot.set_my_commands(scope=BotCommandScopeChat(chat_id), commands=ADMIN_COMMANDS)
        case 'user':
            telegram_bot.set_my_commands(scope=BotCommandScopeChat(chat_id), commands=USER_COMMANDS)
        case 'banned':
            telegram_bot.set_my_commands(scope=BotCommandScopeChat(chat_id), commands=BASE_COMMANDS)
        case _:
            telegram_bot.set_my_commands(scope=BotCommandScopeChat(chat_id), commands=BASE_COMMANDS)
            SetUserCategory(user_id, 'banned')

# Get the user's category
def GetUserCategory(user_id: int) -> str:
    user_info = GetUserInfo(user_id)
    if user_info is None:
        return 'unknown'
    return user_info['user_role']

# Set the user's category
def SetUserCategory(user_id: int, user_role: str) -> bool:
    user_info = GetUserInfo(user_id)
    if user_info is None:
        response = _query_insert(user_id, user_role)
    else:
        response = _query_update(user_id, user_role, user_info['language'], user_info['chat_model'], user_info['remaining_budget'])
    
    if response is None or response['ResponseMetadata']['HTTPStatusCode'] != 200:
        return False
    return True

# Get the information about the user from the database
def GetUserInfo(user_id: int) -> dict | None:
    table = _get_docapi_table()
    try:
        response = table.get_item(Key = {'user_id': Decimal(user_id)})
        return response['Item']['info']
    except ClientError:
        return None
    except KeyError:
        return None

# Query to the database for inserting data about new user
def _query_insert(user_id: int, user_role: str, language: str = 'en', chat_model: str = 'gpt-3.5-turbo', remaining_budget: Decimal = Decimal(0)):
    table = _get_docapi_table()

    response = table.put_item(
        Item = {
            'user_id': Decimal(user_id),
            'info': {
                'user_role': user_role,
                'language': language,
                'chat_model': chat_model,
                'remaining_budget': remaining_budget
            }
        }
    )

    return response

# Query to the database for updating user's information
def _query_update(user_id: int, user_role: str, language: str = 'en', chat_model: str = 'gpt-3.5-turbo', remaining_budget: Decimal = Decimal(0)):
    table = _get_docapi_table()

    response = table.update_item(
        Key = {
            'user_id': Decimal(user_id)
        },
        UpdateExpression = "set info.user_role = :r, info.language = :l, info.chat_model = :m, info.remaining_budget = :b",
        ExpressionAttributeValues = {
            ':r': user_role,
            ':l': language,
            ':m': chat_model,
            ':b': remaining_budget
        },
        ReturnValues = "UPDATED_NEW"
    )

    return response

# Service method for initializing docapi table (table from YDB database)
def _get_docapi_table():
    global docapi_table
    if docapi_table is not None:
        return docapi_table

    docapi_table = _get_boto_session().resource(
        'dynamodb',
        endpoint_url=DOCAPI_ENDPOINT,
        region_name='ru-central1'
    ).Table('users')

    return docapi_table

# Service method for initializing boto session
def _get_boto_session() -> Session:
    global boto_session
    if boto_session is not None:
        return boto_session

    yc_sdk = yandexcloud.SDK()
    channel = yc_sdk._channels.channel("lockbox-payload")
    lockbox = PayloadServiceStub(channel)
    response = lockbox.Get(GetPayloadRequest(secret_id=SECRET_ID))

    access_key = None
    secret_key = None

    for entry in response.entries:
        if entry.key == 'ACCESS_KEY_ID':
            access_key = entry.text_value
        elif entry.key == 'SECRET_ACCESS_KEY':
            secret_key = entry.text_value

    if access_key is None or secret_key is None:
        raise Exception("secrets required")

    boto_session = Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

    return boto_session