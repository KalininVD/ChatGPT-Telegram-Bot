class PluginManager():
    def __init__(self, wolfram_app_id: str, duckduckgo_safesearch: str, worldtime_default_timezone: str):
        self.wolfram_app_id = wolfram_app_id
        self.duckduckgo_safesearch = duckduckgo_safesearch
        self.worldtime_default_timezone = worldtime_default_timezone

        self.plugins = []