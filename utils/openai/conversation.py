from typing import TypedDict
from decimal import Decimal


# Class for representing a message's info
class MessageInfo(TypedDict):
    user_role: str
    message_type: str
    content: str


# Class for representing a message
class Message(TypedDict):
    id: Decimal
    info: MessageInfo


# Class for representing a conversation
class Conversation(TypedDict):
    chat_id: Decimal
    messages: list[Message]