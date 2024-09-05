from logging import Logger

import utils.plugins.plugin_manager
import utils.plugins.wolframalpha
import utils.plugins.duckduckgo
import utils.plugins.weather


# Initialize environment variables
def InitEnvVars(wolfram_api_key: str | None = None, duckduckgo_safesearch: str | None = None, worldtime_default_timezone: str | None = None):
    if wolfram_api_key is None or duckduckgo_safesearch is None or worldtime_default_timezone is None:
        raise ValueError("WolframAlpha API key, DuckDuckGo safesearch, and WorldTime default timezone must be provided")

    utils.plugins.wolframalpha.wolfram_app_id = wolfram_api_key
    utils.plugins.duckduckgo.ddg_safesearch = duckduckgo_safesearch
    utils.plugins.weather.default_timezone = worldtime_default_timezone

# Setup logger
def SetupLogger(logger: Logger):
    utils.plugins.plugin_manager.logger = logger
    utils.plugins.wolframalpha.logger = logger
    utils.plugins.duckduckgo.logger = logger
    utils.plugins.weather.logger = logger