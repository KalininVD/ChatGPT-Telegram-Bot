import os
from dotenv import load_dotenv

from telegram_bot import SetupLogger, InitEnvVars, InitBot, StartBot


# Main function
def main():
    # Load environment variables from .env file
    load_dotenv()

    # Set up logging
    SetupLogger()

    # Initialize environment variables
    InitEnvVars(
        yc_access_key_id=os.environ.get('YC_ACCESS_KEY_ID', None),
        yc_secret_access_key=os.environ.get('YC_SECRET_ACCESS_KEY', None),
        yc_docapi_endpoint=os.environ.get('YC_DOCAPI_ENDPOINT', None),
        telegram_bot_token=os.environ.get('TELEGRAM_BOT_TOKEN', None),
        owner_telegram_id=os.environ.get('OWNER_TELEGRAM_ID', None),
        openai_api_key=os.environ.get('OPENAI_API_KEY', None),
        openai_proxy=os.environ.get('OPENAI_PROXY', None),
        wolfram_api_key=os.environ.get('WOLFRAM_API_KEY', None),
        duckduckgo_safesearch=os.environ.get('DUCKDUCKGO_SAFESEARCH', None),
        worldtime_default_timezone=os.environ.get('WORLDTIME_DEFAULT_TIMEZONE', None),
    )

    # Initialize Telegram Bot
    InitBot()

    # Start the Telegram Bot in case of local debugging
    StartBot()


# Run the main function
if __name__ == '__main__':
    main()