from logging import Logger
from decimal import Decimal
from typing import Generator
from httpx import Client
from openai import OpenAI
from openai.types import CompletionUsage

from utils.openai.models import ChatModelInfo, OPENAI_MODELS, CHAT_MODELS
from utils.openai.conversation import Conversation, Message, MessageInfo
from utils.plugins.plugin_manager import PluginManager
from utils.yandexcloud.conversation_management import ClearConversation, GetConversation, AddMessagesToConversation
from utils.yandexcloud.user_management import SetUserBudget

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
def GetTextResponse(user_id: int, chat_id: Decimal, request: str, chat_model: str, temperature: Decimal, max_tokens: Decimal, budget: Decimal) -> str:
    chat_id = int(chat_id)

    conversation, add_system_prompt, system_prompt, request_message, last_message_id = TakeConversation(chat_id, request)

    openai_args = {
        'model': chat_model,
        'messages': FormatConversation(conversation),
        'temperature': float(temperature),
        'max_tokens': int(max_tokens),
        'n': 1,
        'stream': False,
    }

    # Call OpenAI API
    response = openai.chat.completions.create(**openai_args)
    reply = response.choices[0].message.content
    cost = CalculateTextCost(response.usage, chat_model)
    SetUserBudget(user_id, budget - cost)

    UpdateConversation(last_message_id, chat_id, reply, add_system_prompt, system_prompt, request_message)

    logger.info(f"OpenaAI API call made for user {user_id}. Message length: {len(request)}, response length: {len(reply)}.")
    return reply

# Get the stream text response from the OpenAI API
def GetStreamTextResponse(user_id: int, chat_id: Decimal, request: str, chat_model: str, temperature: Decimal, max_tokens: Decimal, budget: Decimal) -> Generator[str, None, None]:
    chat_id = int(chat_id)

    conversation, add_system_prompt, system_prompt, request_message, last_message_id = TakeConversation(chat_id, request)

    reply = ''
    usage = None

    openai_args = {
        'model': chat_model,
        'messages': FormatConversation(conversation),
        'temperature': float(temperature),
        'max_tokens': int(max_tokens),
        'n': 1,
        'stream': True,
        'stream_options': {'include_usage': True},
    }

    # Call OpenAI API
    for chunk in openai.chat.completions.create(**openai_args):
        choices = chunk.choices
        usage = chunk.usage

        if usage is not None and len(choices) == 0:
            break
        
        text = choices[0].delta.content
        reply += text
        yield text
    
    cost = CalculateTextCost(usage, chat_model)
    SetUserBudget(user_id, budget - cost)

    UpdateConversation(last_message_id, chat_id, reply, add_system_prompt, system_prompt, request_message)
    
    logger.info(f"OpenaAI API call made for user {user_id}. Message length: {len(request)}, response length: {len(reply)}.")
    return reply

# Service method for taking the conversation from the database
def TakeConversation(chat_id: int, request: str) -> tuple[Conversation, bool, Message | None, Decimal]:
    conversation = GetConversation(chat_id)

    system_prompt = None
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

    return conversation, add_system_prompt, system_prompt, request_message, last_message_id

# Update the conversation history with the reply from the OpenAI API
def UpdateConversation(last_message_id: Decimal, chat_id: int, reply: str, add_system_prompt: bool, system_prompt: Message | None, request_message: Message):
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
def SummarizeConversation(user_id: int, chat_id: int, budget: Decimal):
    conversation = GetConversation(chat_id)
    
    system_prompt = conversation['messages'][0]['info']['content'] if any(conversation['messages']) else None

    ResetConversation(user_id, chat_id, system_prompt)

    if len(conversation['messages']) <= 1:
        logger.warning(f"Conversation history for user #{user_id} is empty")
        return
    
    summary_response = openai.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'assistant', 'content': "Summarize this conversation in 700 characters or less"},
            {'role': 'user', 'content': str(FormatConversation(conversation))},
        ],
        temperature=0.4,
        n=1,
    )

    if summary_response.choices[0].message.content is None:
        logger.warning(f"Failed to summarize conversation history for user #{user_id}")
        return
    
    cost = CalculateTextCost(summary_response.usage, 'gpt-4o-mini')
    SetUserBudget(user_id, budget - cost)

    summary_message = Message(
        id=Decimal('1'),
        info=MessageInfo(
            user_role='assistant',
            message_type='text',
            content=summary_response.choices[0].message.content,
        ),
    )

    AddMessagesToConversation(
        chat_id=chat_id,
        messages=[summary_message],
    )
    
    logger.info(f"Successfully summarized conversation history for user #{user_id}")