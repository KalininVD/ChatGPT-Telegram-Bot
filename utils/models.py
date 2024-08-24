# Import necessary modules, classes and functions
from decimal import Decimal

# Define the base class for the model info
class ModelInfo():
    def __init__(self, model_name: str, type: str):
        self.model_type = type
        self.model_name = model_name

# Class for chat models info
class ChatModelInfo(ModelInfo):
    def __init__(self, model_name: str, input_price: Decimal | str, output_price: Decimal, context_window: int, max_output_tokens: int, vision_available: bool = False):
        super().__init__(model_name, 'chat')

        self.input_price = Decimal(input_price)
        self.output_price = output_price
        self.context_window = context_window
        self.max_output_tokens = max_output_tokens
        self.vision_available = vision_available

# Class for image models info
class ImageModelInfo(ModelInfo):
    def __init__(self, model_name: str, quality: str | None, resolution: str, price: Decimal | str, max_output_images: int):
        super().__init__(model_name, 'image')

        self.quality = quality
        self.resolution = resolution
        self.price = Decimal(price)
        self.max_output_images = max_output_images

# Class for audio models info (TTS, STT and translation)
class AudioModelInfo(ModelInfo):
    def __init__(self, task: str, model_name: str, price: Decimal | str):
        super().__init__(model_name, 'audio')

        self.task = task
        self.price = Decimal(price)

# Define the dictionary of all available OpenAI models
OPENAI_MODELS = {
    'gpt-4o': ChatModelInfo('gpt-4o', '5', '15', 128000, 4096, True),
    'gpt-4o-2024-05-13': ChatModelInfo('gpt-4o-2024-05-13', '5', '15', 128000, 4096, True),
    'gpt-4o-2024-08-06': ChatModelInfo('gpt-4o-2024-08-06', '2.5', '10', 128000, 16384, True),

    'gpt-4o-mini': ChatModelInfo('gpt-4o-mini', '0.15', '0.6', 128000, 16384, True),
    'gpt-4o-mini-2024-07-18': ChatModelInfo('gpt-4o-mini-2024-07-18', '0.15', '0.6', 128000, 16384, True),

    'gpt-4-turbo': ChatModelInfo('gpt-4-turbo', '10', '30', 128000, 4096, True),
    'gpt-4-turbo-2024-04-09': ChatModelInfo('gpt-4-turbo-2024-04-09', '10', '30', 128000, 4096, True),

    'gpt-4-0125-preview': ChatModelInfo('gpt-4-0125-preview', '10', '30', 128000, 4096),
    'gpt-4-1106-preview': ChatModelInfo('gpt-4-1106-preview', '10', '30', 128000, 4096),

    'gpt-4': ChatModelInfo('gpt-4', '30', '60', 8192, 8192),
    'gpt-4-0613': ChatModelInfo('gpt-4-0613', '30', '60', 8192, 8192),

    'gpt-3.5-turbo': ChatModelInfo('gpt-3.5-turbo', '0.5', '1.5', 16385, 4096),
    'gpt-3.5-turbo-0125': ChatModelInfo('gpt-3.5-turbo-0125', '0.5', '1.5', 16385, 4096),
    'gpt-3.5-turbo-1106': ChatModelInfo('gpt-3.5-turbo-1106', '1', '2', 16385, 4096),

    'gpt-3.5-turbo-instruct': ChatModelInfo('gpt-3.5-turbo-instruct', '1.5', '2', 4096, 4096),

    'dall-e-3-Standard-1024×1024': ImageModelInfo('dall-e-3', 'standard', '1024x1024', '0.04', 1),
    'dall-e-3-Standard-1024×1792': ImageModelInfo('dall-e-3', 'standard', '1024x1792', '0.08', 1),
    'dall-e-3-Standard-1792×1024': ImageModelInfo('dall-e-3', 'standard', '1792×1024', '0.08', 1),

    'dall-e-3-HD-1024×1024': ImageModelInfo('dall-e-3', 'HD', '1024×1024', '0.08', 1),
    'dall-e-3-HD-1024×1792': ImageModelInfo('dall-e-3', 'HD', '1024×1792', '0.12', 1),
    'dall-e-3-HD-1792×1024': ImageModelInfo('dall-e-3', 'HD', '1792×1024', '0.12', 1),

    'dall-e-2-1024×1024': ImageModelInfo('dall-e-2', None, '1024×1024', '0.02', 10),
    'dall-e-2-512×512': ImageModelInfo('dall-e-2', None, '512×512', '0.018', 10),
    'dall-e-2-256×256': ImageModelInfo('dall-e-2', None, '256×256', '0.016', 10),

    'Whisper': AudioModelInfo('transcription', 'whisper-1', '0.006'),
    'whisper-1': AudioModelInfo('transcription', 'whisper-1', '0.006'),
    'Whisper': AudioModelInfo('translation', 'whisper-1', '0.006'),
    'whisper-1': AudioModelInfo('translation', 'whisper-1', '0.006'),

    'tts-1': AudioModelInfo('tts', 'tts-1', '15'),
    'tts-1-hd': AudioModelInfo('tts', 'tts-1-hd', '30'),
}