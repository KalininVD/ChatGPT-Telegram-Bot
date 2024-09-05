from logging import Logger
from decimal import Decimal
from httpx import Client
from openai import OpenAI
from openai.types import CompletionUsage

from utils.openai.models import ChatModelInfo, OPENAI_MODELS, CHAT_MODELS
from utils.openai.conversation import Conversation, Message, MessageInfo
from utils.plugins.plugin_manager import PluginManager
from utils.yandexcloud.conversation_management import ClearConversation, GetConversation, AddMessagesToConversation

# Define services
logger: Logger
api_key: str
proxy: str
openai: OpenAI
plugin_manager: PluginManager

# Initialize OpenAI Helper
def InitHelper():
    global openai, plugin_manager

    openai = OpenAI(
        api_key=api_key,
        http_client=Client(proxy=proxy)
    )
    
    plugin_manager = PluginManager()

    logger.info("Successfully initialized OpenAI Helper")

# Calculate the cost of the text response
def CalculateTextCost(usage: CompletionUsage, model: str) -> Decimal:
    if model not in CHAT_MODELS:
        return Decimal('0')
    
    model: ChatModelInfo = OPENAI_MODELS[model]

    input_cost = Decimal(usage.prompt_tokens) * Decimal(model.input_price) / Decimal('1000000')
    output_cost = Decimal(usage.completion_tokens) * Decimal(model.output_price) / Decimal('1000000')
    total_cost = input_cost + output_cost

    return total_cost

# Service method for formatting the conversation to the OpenAI API format
def FormatConversation(conversation: Conversation) -> list[dict[str, str]]:
    return list(
        map(
            lambda message: {
                'role': message['info']['user_role'],
                'content': message['info']['content'],
            },
            conversation['messages']
        )
    )

# Get the text response from the OpenAI API
def GetTextResponse(user_id: int, chat_id: int, message_id: int, request: str, chat_model: str) -> tuple[str, CompletionUsage]:
    conversation = GetConversation(chat_id)

    add_system_prompt = not any(conversation['messages'])
    if add_system_prompt:
        system_prompt = Message(
            id=Decimal('0'),
            info=MessageInfo(
                user_role='system',
                message_type='text',
                content="You are a helpful assistant.",
            ),
        )
        conversation['messages'] = [system_prompt]
    
    last_message_id = conversation['messages'][-1]['id']

    request_message = Message(
        id=last_message_id + Decimal('1'),
        info=MessageInfo(
            user_role='user',
            message_type='text',
            content=request,
        ),
    )

    conversation['messages'].append(request_message)

    # Call OpenAI API
    response = openai.chat.completions.create(
        model=chat_model,
        messages=FormatConversation(conversation),
    )
    reply = response.choices[0].message.content
    usage = response.usage

    reply_message = Message(
        id=last_message_id + Decimal('2'),
        info=MessageInfo(
            user_role='assistant',
            message_type='text',
            content=reply,
        ),
    )

    if add_system_prompt:
        AddMessagesToConversation(
            chat_id=chat_id,
            messages=[system_prompt, request_message, reply_message],
        )
    else:
        AddMessagesToConversation(
            chat_id=chat_id,
            messages=[request_message, reply_message],
        )

    logger.info(f"OpenaAI API call made for user {user_id}. Message length: {len(request)}, response length: {len(reply)}.")
    return reply, usage

# Reset the conversation history with custom system prompt
def ResetConversation(user_id: int, chat_id: int, system_prompt: str | None = None):
    ClearConversation(chat_id)

    AddMessagesToConversation(
        chat_id=chat_id,
        messages=[
            Message(
                id=Decimal('0'),
                info=MessageInfo(
                    user_role='system',
                    message_type='text',
                    content=system_prompt or "You are a helpful assistant.",
                ),
            ),
        ],
    )

    logger.info(f"Successfully reset conversation history for user #{user_id} with {'custom' if system_prompt else 'default'} system prompt")

# Summarize the conversation history
def SummarizeConversation(user_id: int, chat_id: int):
    messages = GetConversation(chat_id)['messages']

    ResetConversation(
        user_id=user_id,
        chat_id=chat_id,
        system_prompt=messages[0]['info']['content'] if any(messages) else None,
    )
    
    logger.info(f"Successfully summarized conversation history for user #{user_id}")