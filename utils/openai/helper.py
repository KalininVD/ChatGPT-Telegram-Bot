from logging import Logger
from decimal import Decimal
from httpx import Client
from openai import OpenAI
from openai.types import CompletionUsage

from utils.openai.models import ChatModelInfo, OPENAI_MODELS, CHAT_MODELS
from utils.plugins.plugin_manager import PluginManager

# Define services
logger: Logger
api_key: str
proxy: str
openai: OpenAI
conversations: dict[int, list[dict[str, str]]] = {}
plugin_manager: PluginManager

# Initialize OpenAI Helper
def InitHelper():
    global openai, conversations, plugin_manager

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

# Get the text response from the OpenAI API
def GetTextResponse(user_id: int, message: str, chat_model: str) -> tuple[str, CompletionUsage]:
    if user_id not in conversations:
        ResetConversation(user_id)

    conversations[user_id].append(
        {
            "role": "user",
            "content": message
        }
    )

    # Call OpenAI API
    response = openai.chat.completions.create(
        model=chat_model,
        messages=conversations[user_id]
    )
    reply = response.choices[0].message.content
    usage = response.usage

    conversations[user_id].append(
        {
            "role": "assistant",
            "content": reply
        }
    )

    logger.info(f"OpenaAI API call made for user {user_id}. Message length: {len(message)}, response length: {len(reply)}")
    return reply, usage

# Reset the conversation history with custom system prompt
def ResetConversation(user_id: int, system_prompt: str | None = None):
    conversations[user_id] = [
        {
            "role": "system",
            "content": system_prompt or "You are a helpful assistant."
        }
    ]

    logger.info(f"Successfully reset conversation history for user #{user_id} with custom system prompt")

# Summarize the conversation history
def SummarizeConversation(user_id: int):
    ResetConversation(
        user_id=user_id,
        system_prompt=conversations[user_id][0]['content'] if user_id in conversations else None,
    )
    
    logger.info(f"Successfully summarized conversation history for user #{user_id}")