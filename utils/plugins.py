# Import necessary modules, classes and functions
import wolframalpha
import duckduckgo_search

# Define environment variables
WOLFRAM_APP_ID: str | None = None
DUCKDUCKGO_SAFESEARCH: str | None = None
WORLDTIME_DEFAULT_TIMEZONE: str | None = None

# Initialize environment variables
def InitEnvVars(vars: dict):
    global WOLFRAM_APP_ID, DUCKDUCKGO_SAFESEARCH, WORLDTIME_DEFAULT_TIMEZONE
    
    WOLFRAM_APP_ID = vars.get('WOLFRAM_APP_ID')
    DUCKDUCKGO_SAFESEARCH = vars.get('DUCKDUCKGO_SAFESEARCH')
    WORLDTIME_DEFAULT_TIMEZONE = vars.get('WORLDTIME_DEFAULT_TIMEZONE')

# The main class for managing plugins
class PluginManager():
    def __init__(self):
        self.plugins = []