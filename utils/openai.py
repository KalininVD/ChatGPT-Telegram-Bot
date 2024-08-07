# Import necessary modules, classes and functions
import openai

# Define environment variables
OPENAI_API_KEY: str | None = None

# Initialize environment variables
def InitEnvVars(vars: dict):
    global OPENAI_API_KEY
    
    OPENAI_API_KEY = vars.get('OPENAI_API_KEY')

# The main class for interacting with OpenAI API
class OpenAIHelper():
    def __init__(self):
        self.openai = OPENAI_API_KEY