from decimal import Decimal
from logging import Logger
from boto3.dynamodb.conditions import Key

from utils.users import User, UserInfo, INFO_DEFAULTS, USER_ROLES
from utils.translations import supported_languages
from utils.openai.models import CHAT_MODELS, VISION_MODELS, IMAGE_MODELS, TRANSLATE_MODELS, STT_MODELS, TTS_MODELS
from utils.openai.chat_model_params import TEMPERATURES, TOKEN_LIMITS

# Define services
logger: Logger
user_settings_table = None

# Get the user's information by ID
def GetUserByID(user_id: int | Decimal) -> User | None:
    table = user_settings_table

    response = table.get_item(
        Key = {
            'user_id': Decimal(user_id)
        }
    )

    item = response.get('Item', None)

    if item is None:
        logger.warning(f"User #{user_id} is not registered yet")
        return None
    
    return User(
        id=user_id,
        info=UserInfo(item['info'])
    )

# Add new user to the database
def AddNewUser(user_id: str | int | Decimal, user_name: str, chat_id: str | int | Decimal, user_role: str = 'banned') -> User | None:
    if len(user_name) > 32 or int(chat_id) < 0 or user_role not in USER_ROLES:
        return None

    user_info = INFO_DEFAULTS.copy()
    user_info['user_name'] = user_name
    user_info['chat_id'] = Decimal(chat_id)
    user_info['user_role'] = user_role

    table = user_settings_table

    response = table.put_item(
        Item = {
            'user_id': Decimal(user_id),
            'info': user_info,
        }
    )

    if response.get('ResponseMetadata', {}).get('HTTPStatusCode', None) != 200:
        logger.error(f"Failed to register user #{user_id}")
        return None

    return User(
        id=user_id,
        info=UserInfo(user_info),
    )

def UpdateUserInfo(user_id: int | Decimal, user_info: UserInfo) -> bool:
    table = user_settings_table

    response = table.update_item(
        Key = {
            'user_id': Decimal(user_id),
        },
        UpdateExpression = "set " + ', '.join(
            f"info.{key} = :{value}" for key, value in {
                'user_name': 'n',
                'chat_id': 'c',
                'user_role': 'r',
                'bot_language': 'l',
                'chat_model': 'm',
                'vision_model': 'v',
                'image_model': 'i',
                'translate_model': 't',
                'stt_model': 's',
                'tts_model': 'g',
                'temperature': 'e',
                'token_limit': 'p',
                'user_budget': 'b',
            }.items()
        ),
        ExpressionAttributeValues = {
            ':n': user_info['user_name'],
            ':c': user_info['chat_id'],
            ':r': user_info['user_role'],
            ':l': user_info['bot_language'],
            ':m': user_info['chat_model'],
            ':v': user_info['vision_model'],
            ':i': user_info['image_model'],
            ':t': user_info['translate_model'],
            ':s': user_info['stt_model'],
            ':g': user_info['tts_model'],
            ':e': user_info['temperature'],
            ':p': user_info['token_limit'],
            ':b': user_info['user_budget'],
        },
        ReturnValues = "UPDATED_NEW",
    )

    logger.info(f"Successfully updated information about user #{user_id}")

    return response.get('ResponseMetadata', {}).get('HTTPStatusCode', None) == 200

# Set the user's name
def SetUserName(user_id: int | Decimal, user_name: str) -> bool:
    if len(user_name) > 32:
        return False
    
    user = GetUserByID(user_id)
    if user is None:
        user = AddNewUser(user_id)
        if user is None:
            return False
    
    user_info = UserInfo(user['info'])

    if user_info['user_name'] == user_name:
        return True
    
    user_info['user_name'] = user_name
    return UpdateUserInfo(user_id, user_info)

# Set the user's chat ID
def SetUserChatID(user_id: int | Decimal, chat_id: int | str | Decimal) -> bool:
    chat_id = Decimal(chat_id)

    user = GetUserByID(user_id)
    if user is None:
        user = AddNewUser(user_id)
        if user is None:
            return False
        
    user_info = UserInfo(user['info'])

    if user_info['chat_id'] == chat_id:
        return True
    
    user_info['chat_id'] = chat_id
    return UpdateUserInfo(user_id, user_info)

# Set the user's category
def SetUserRole(user_id: int | Decimal, user_role: str) -> bool:
    if user_role not in USER_ROLES:
        return False
    
    user = GetUserByID(user_id)
    if user is None:
        user = AddNewUser(user_id)
        if user is None:
            return False
    
    user_info = UserInfo(user['info'])

    if user_info['user_role'] == user_role:
        return True
    
    user_info['user_role'] = user_role
    return UpdateUserInfo(user_id, user_info)

# Set the user's language
def SetUserLanguage(user_id: int | Decimal, language: str) -> bool:
    if language not in supported_languages:
        return False
    
    user = GetUserByID(user_id)
    if user is None:
        user = AddNewUser(user_id)
        if user is None:
            return False
    
    user_info = UserInfo(user['info'])

    if user_info['bot_language'] == language:
        return True
    
    user_info['bot_language'] = language
    return UpdateUserInfo(user_id, user_info)

# Set the user's chat model
def SetUserChatModel(user_id: int | Decimal, chat_model: str) -> bool:
    if chat_model not in CHAT_MODELS:
        return False
    
    user = GetUserByID(user_id)
    if user is None:
        user = AddNewUser(user_id)
        if user is None:
            return False
        
    user_info = UserInfo(user['info'])

    if user_info['chat_model'] == chat_model:
        return True
    
    user_info['chat_model'] = chat_model
    return UpdateUserInfo(user_id, user_info)

# Set the user's vision model
def SetUserVisionModel(user_id: int | Decimal, vision_model: str) -> bool:
    if vision_model not in VISION_MODELS:
        return False
    
    user = GetUserByID(user_id)
    if user is None:
        user = AddNewUser(user_id)
        if user is None:
            return False
        
    user_info = UserInfo(user['info'])

    if user_info['vision_model'] == vision_model:
        return True
    
    user_info['vision_model'] = vision_model
    return UpdateUserInfo(user_id, user_info)

# Set the user's image model
def SetUserImageModel(user_id: int | Decimal, image_model: str) -> bool:
    if image_model not in IMAGE_MODELS:
        return False
    
    user = GetUserByID(user_id)
    if user is None:
        user = AddNewUser(user_id)
        if user is None:
            return False
        
    user_info = UserInfo(user['info'])

    if user_info['image_model'] == image_model:
        return True
    
    user_info['image_model'] = image_model
    return UpdateUserInfo(user_id, user_info)

# Set the user's translate model
def SetUserTranslateModel(user_id: int | Decimal, translate_model: str) -> bool:
    if translate_model not in TRANSLATE_MODELS:
        return False
    
    user = GetUserByID(user_id)
    if user is None:
        user = AddNewUser(user_id)
        if user is None:
            return False
        
    user_info = UserInfo(user['info'])

    if user_info['translate_model'] == translate_model:
        return True
    
    user_info['translate_model'] = translate_model
    return UpdateUserInfo(user_id, user_info)

# Set the user's STT model
def SetUserSTTModel(user_id: int | Decimal, stt_model: str) -> bool:
    if stt_model not in STT_MODELS:
        return False
    
    user = GetUserByID(user_id)
    if user is None:
        user = AddNewUser(user_id)
        if user is None:
            return False
        
    user_info = UserInfo(user['info'])

    if user_info['stt_model'] == stt_model:
        return True
    
    user_info['stt_model'] = stt_model
    return UpdateUserInfo(user_id, user_info)

# Set the user's TTS model
def SetUserTTSModel(user_id: int | Decimal, tts_model: str) -> bool:
    if tts_model not in TTS_MODELS:
        return False
    
    user = GetUserByID(user_id)
    if user is None:
        user = AddNewUser(user_id)
        if user is None:
            return False
        
    user_info = UserInfo(user['info'])

    if user_info['tts_model'] == tts_model:
        return True
    
    user_info['tts_model'] = tts_model
    return UpdateUserInfo(user_id, user_info)

# Set the user's chat model temperature
def SetUserTemperature(user_id: int | Decimal, temperature: str | int | Decimal) -> bool:
    temperature = Decimal(temperature)
    
    if temperature not in TEMPERATURES:
        return False
    
    user = GetUserByID(user_id)
    if user is None:
        user = AddNewUser(user_id)
        if user is None:
            return False
        
    user_info = UserInfo(user['info'])

    if user_info['temperature'] == temperature:
        return True
    
    user_info['temperature'] = temperature
    return UpdateUserInfo(user_id, user_info)

# Set the user's chat model token limit
def SetUserTokenLimit(user_id: int | Decimal, token_limit: str | int | Decimal) -> bool:
    token_limit = Decimal(token_limit)

    if token_limit not in TOKEN_LIMITS:
        return False
    
    user = GetUserByID(user_id)
    if user is None:
        user = AddNewUser(user_id)
        if user is None:
            return False
        
    user_info = UserInfo(user['info'])

    if user_info['token_limit'] == token_limit:
        return True
    
    user_info['token_limit'] = token_limit
    return UpdateUserInfo(user_id, user_info)

# Set the user's budget
def SetUserBudget(id: int | Decimal, budget: Decimal) -> bool:
    if budget < Decimal(0):
        budget = Decimal(0)

    user = GetUserByID(id)
    if user is None:
        user = AddNewUser(id)
        if user is None:
            return False
    
    user_info = UserInfo(user['info'])

    if user_info['user_budget'] == budget:
        return True
    
    user_info['user_budget'] = budget
    return UpdateUserInfo(id, user_info)

# Get the information about the users of the specified category from the database
def GetUsersByCategory(user_role: str) -> list[User]:
    table = user_settings_table

    scan_kwargs = {
        'FilterExpression': Key('info.user_role').eq(user_role),
        'ProjectionExpression': "user_id, " + ', '.join(
            f"info.{key}" for key in INFO_DEFAULTS.keys()
        ),
    }

    users = []

    done = False
    start_key = None

    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key

        response = table.scan(**scan_kwargs)
        
        for user in response.get('Items', []):
            users.append(
                User(
                    id=user['user_id'],
                    info=UserInfo(user['info']),
                )
            )

        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None
    
    logger.info(f"Successfully retrieved information about {len(users)} users of category '{user_role}'")

    return users

def DeleteUser(user_id: int | Decimal) -> bool:
    table = user_settings_table

    response = table.delete_item(
        Key = {
            'user_id': Decimal(user_id),
        }
    )

    logger.warning(f"Successfully deleted user #{user_id}")

    return response.get('ResponseMetadata', {}).get('HTTPStatusCode', None) == 200