```markdown
# ChatGPT-Telegram-Bot

The ChatGPT-Telegram-Bot is a Telegram bot designed to enable seamless interaction with the ChatGPT model via the OpenAI API. Hosted on Yandex Cloud, this bot supports multiple languages and user role management, allowing users to send various types of media and receive contextually relevant responses powered by OpenAI's language model.

## Overview

The architecture of the ChatGPT-Telegram-Bot follows a modular design, with separate modules handling different functionalities, such as command handling, user management, translations, and OpenAI interactions. The bot is developed using Python and utilizes the `pyTelegramBotAPI` library for Telegram interactions. It integrates with the OpenAI API for generating responses and uses Yandex Cloud's DynamoDB for persistent data storage.

The project structure includes the following key components:
- **`main.py`**: The entry point for initializing the bot and setting up command handlers.
- **`telegram_bot.py`**: Implements the core functionalities of the bot, including message handling and command processing.
- **`utils/`**: A directory containing utility modules for translations, OpenAI interactions, user management, and Yandex Cloud integration.
- **`translations.json`**: Contains localization data for supporting multiple languages.

## Features

1. **User Interaction**: Users can send text messages, photos, audio, and video to the bot, which processes and responds accordingly.
2. **Command Handling**: The bot supports various commands such as `/start`, `/help`, `/language`, `/budget`, `/reset`, `/summarize`, `/settings`, and `/users`.
3. **Multilingual Support**: Currently supports English and Russian, allowing users to switch languages easily.
4. **User Role Management**: Different user roles (owner, admin, user, banned) are managed, providing tailored command sets.
5. **Budget Management**: Users can view and manage their interaction budget.
6. **Inline Keyboards**: Provides intuitive navigation through inline keyboards for command selection.
7. **OpenAI Integration**: Communicates with the OpenAI API to process user queries and generate responses.
8. **Database Integration**: User information is stored in a DynamoDB database for persistent management.
9. **Logging System**: Implements a logging system for tracing application actions within Yandex Cloud.

## Getting started

### Requirements

To run the ChatGPT-Telegram-Bot, ensure you have the following technologies installed:
- Python
- Yandex Cloud CLI
- Required Python libraries as listed in `requirements.txt`

### Quickstart

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ChatGPT-Telegram-Bot
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables for the bot, including API keys for OpenAI, Yandex Cloud, and Telegram.

4. Run the bot:
   ```bash
   python main.py
   ```

### License

Copyright (c) 2024.
```