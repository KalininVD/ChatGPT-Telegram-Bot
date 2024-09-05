from typing import TypedDict
from decimal import Decimal

# Class for storing all user information
class UserInfo(TypedDict):
    user_name: str
    chat_id: Decimal
    
    user_role: str
    bot_language: str
    
    chat_model: str
    vision_model: str
    image_model: str
    translate_model: str
    stt_model: str
    tts_model: str
    temperature: Decimal
    token_limit: Decimal
    
    user_budget: Decimal

# Class for storing user information in (id, info) format
class User(TypedDict):
    id: Decimal
    info: UserInfo

INFO_DEFAULTS = {
    'user_name': 'unknown',
    'chat_id': Decimal('0'),
    'user_role': 'banned',
    'bot_language': 'en',
    'chat_model': "gpt-4o-mini",
    'vision_model': "gpt-4o-mini",
    'image_model': "dall-e-2-256-256",
    'translate_model': "whisper-1",
    'stt_model': "whisper-1",
    'tts_model': "tts-1",
    'temperature': Decimal('0.5'),
    'token_limit': Decimal('100'),
    'user_budget': Decimal('0'),
}

USER_ROLES = ('owner', 'admin', 'user', 'banned', )