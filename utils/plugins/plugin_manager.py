from logging import Logger

# Define logger
logger: Logger

# The main class for managing plugins
class PluginManager():
    def __init__(self):
        self.plugins = []

        logger.info("Successfully initialized Plugin Manager")