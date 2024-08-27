# Import necessary modules, classes and functions
from decimal import Decimal
from openai import OpenAI
from openai.types import CompletionUsage
from httpx import Client
import logging
from utils.models import OPENAI_MODELS

# Define environment variables
OPENAI_API_KEY: str | None = None
PROXY: str | None = None

# Initialize environment variables
def InitEnvVars(vars: dict):
    global OPENAI_API_KEY, PROXY
    
    OPENAI_API_KEY = vars.get('OPENAI_API_KEY')
    PROXY = vars.get('PROXY')

# Define all available models
ALL_MODELS = list(OPENAI_MODELS.keys())

# Define all models by their type
CHAT_MODELS = list(model for model in ALL_MODELS if OPENAI_MODELS[model].model_type == 'chat')
VISION_MODELS = list(model for model in CHAT_MODELS if OPENAI_MODELS[model].vision_available)
IMAGE_MODELS = list(model for model in ALL_MODELS if OPENAI_MODELS[model].model_type == 'image')
AUDIO_MODELS = list(model for model in ALL_MODELS if OPENAI_MODELS[model].model_type == 'audio')
STT_MODELS = list(model for model in AUDIO_MODELS if OPENAI_MODELS[model].task == 'transcription')
TTS_MODELS = list(model for model in AUDIO_MODELS if OPENAI_MODELS[model].task == 'tts')


# The main class for interacting with OpenAI API
class OpenAIHelper():
    def __init__(self, logger: logging.Logger):
        self.openai = OpenAI(
            api_key=OPENAI_API_KEY,
            http_client=Client(proxy=PROXY)
        )

        self.logger = logger

        self.conversations: dict[int, list[dict[str, str]]] = {}
    
    def calculate_text_cost(self, usage: CompletionUsage, model: str) -> Decimal:
        if model not in CHAT_MODELS:
            return Decimal(0)

        input_cost = Decimal(usage.prompt_tokens) * Decimal(OPENAI_MODELS[model].input_price) / Decimal('1000000')
        output_cost = Decimal(usage.completion_tokens) * Decimal(OPENAI_MODELS[model].output_price) / Decimal('1000000')
        total_cost = input_cost + output_cost

        return total_cost
    
    def get_text_response(self, user_id: int, message: str, model_name: str) -> tuple[str, CompletionUsage]:
        if user_id not in self.conversations:
            self.reset_conversation(user_id)

        self.conversations[user_id].append(
            {
                "role": "user",
                "content": message
            }
        )

        # Call OpenAI API
        response = self.openai.chat.completions.create(
            model=model_name,
            messages=self.conversations[user_id]
        )
        reply = response.choices[0].message.content
        usage = response.usage

        self.conversations[user_id].append(
            {
                "role": "assistant",
                "content": reply
            }
        )

        self.logger.info(f"OpenaAI API call made for user {user_id}. Message length: {len(message)}, response length: {len(reply)}")
        return reply, usage
    
    def reset_conversation(self, user_id: int):
        self.conversations[user_id] = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            }
        ]