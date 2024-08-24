# Import necessary modules, classes and functions
from openai import OpenAI
from httpx import Client
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
    def __init__(self):
        self.openai = OpenAI(
            api_key=OPENAI_API_KEY,
            http_client=Client(proxy=PROXY)
        )

        self.conversations: dict[int, list[dict[str, str]]] = {}