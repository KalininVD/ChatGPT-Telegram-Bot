```markdown
# ChatGPT-Telegram-Bot

The ChatGPT-Telegram-Bot is a Telegram bot that enables users to interact with the ChatGPT model via the OpenAI API. It is hosted on Yandex Cloud and offers features such as multilingual support, user role management, and integration with external services, providing a seamless conversational experience.

## Overview

The architecture of the ChatGPT-Telegram-Bot follows a modular design, with separate modules handling different functionalities, such as command handling, user management, and translations. The bot is developed using Python and utilizes the `pyTelegramBotAPI` library for Telegram interactions, along with the OpenAI API for generating responses. The project structure includes various utility files for managing translations, plugins, and database interactions with DynamoDB on Yandex Cloud.

### Technologies Used
- **Python**: The primary programming language for developing the bot.
- **Yandex Cloud CLI**: Command-line interface for managing Yandex Cloud resources.
- **pyTelegramBotAPI**: A Python wrapper for the Telegram Bot API.
- **requests**: An HTTP library for making API calls to OpenAI and other services.
- **boto3**: The AWS SDK for Python, used for interacting with DynamoDB.

## Features

- **User Interaction**: Users can send text messages, photos, audio, and video to the bot, which processes and responds accordingly.
- **Command Handling**: Supports commands like `/start`, `/help`, `/language`, `/budget`, `/reset`, `/summarize`, `/settings`, and `/users`.
- **Multilingual Support**: Currently supports English and Russian, allowing users to switch languages.
- **User Role Management**: Distinguishes between owner, admin, user, and banned roles, providing different command sets based on user roles.
- **Budget Management**: Users can view and manage their budget for using the bot's services.
- **Inline Keyboards**: Utilizes inline keyboards for intuitive navigation and command selection.
- **Integration with OpenAI**: Communicates with the OpenAI API to process and generate responses.
- **Database Integration**: User data is stored in a DynamoDB database, allowing for persistent data management.
- **Logging System**: Implements a logging system to trace application actions within Yandex Cloud.

## Getting started

### Requirements

To run the ChatGPT-Telegram-Bot, ensure you have the following technologies installed:
- Python 3.x
- Yandex Cloud CLI
- Required Python packages listed in `requirements.txt`

### Quickstart

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ChatGPT-Telegram-Bot
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables. Ensure the following variables are defined:
   - `TELEGRAM_BOT_TOKEN`
   - `OWNER_TELEGRAM_ID`
   - `OWNER_TELEGRAM_NAME`
   - OpenAI API key and Yandex Cloud credentials.

4. Run the bot:
   ```bash
   python main.py
   ```

### License

Copyright (c) 2024. All rights reserved.
```