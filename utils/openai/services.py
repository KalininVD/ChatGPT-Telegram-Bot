from logging import Logger

import utils.openai.helper
import utils.plugins.services


# Initialize environment variables
def InitEnvVars(openai_api_key: str | None = None, openai_proxy: str | None = None):
    if openai_api_key is None or openai_proxy is None:
        raise ValueError("OpenAI API key and proxy must be provided")

    utils.openai.helper.api_key = openai_api_key
    utils.openai.helper.proxy = openai_proxy

# Setup logger
def SetupLogger(logger: Logger):
    utils.plugins.services.SetupLogger(logger)
    utils.openai.helper.logger = logger