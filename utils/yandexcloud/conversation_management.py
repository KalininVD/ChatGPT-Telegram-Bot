from decimal import Decimal
from logging import Logger

from utils.openai.conversation import Message, Conversation
from utils.yandexcloud.services import GetTable, CreateNewTable, DeleteTable


# Define services
logger: Logger


# Add any number of messages to the conversation in the specified chat
def AddMessagesToConversation(chat_id: int | Decimal, messages: list[Message]):
    table = GetTable(chat_id)

    for message in messages:
        response = table.put_item(
            Item = dict(message),
        )

        if response.get('ResponseMetadata', {}).get('HTTPStatusCode', None) != 200:
            logger.error(f"Failed to add message to conversation for chat #{chat_id}")
            return
        
        logger.info(f"Successfully added message to conversation for chat #{chat_id}")

# Get the conversation from the specified chat
def GetConversation(chat_id: int | Decimal):
    table = GetTable(chat_id)

    scan_kwargs = {
        'ProjectionExpression': "id, info.user_role, info.message_type, info.content",
    }

    done = False
    start_key = None

    messages = []

    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        
        response = table.scan(**scan_kwargs)
        messages.extend(response.get('Items', []))
        
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None
    
    logger.info(f"Successfully retrieved conversation for chat #{chat_id}: {len(messages)} messages")

    return Conversation(
        chat_id=chat_id,
        messages=messages,
    )

# Clear the conversation in the specified chat
def ClearConversation(chat_id: int | Decimal):
    table_name = str(chat_id)
    DeleteTable(table_name)
    CreateNewTable(table_name)

# Delete the conversation in the specified chat
def DeleteConversation(chat_id: int | Decimal):
    DeleteTable(str(chat_id))