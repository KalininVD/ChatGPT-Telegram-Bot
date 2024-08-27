```markdown
# ChatGPT-Telegram-Bot

The ChatGPT-Telegram-Bot is a Telegram bot that allows users to interact with the ChatGPT model via the OpenAI API. Hosted on Yandex Cloud, this bot enables users to send various types of queries and receive intelligent responses, providing a seamless conversational experience while managing their settings and budget.

## Overview

The architecture of the ChatGPT-Telegram-Bot is modular, with separate components handling user interaction, command processing, OpenAI API communication, and database management. The bot is developed using Python and leverages several technologies, including the `pyTelegramBotAPI` for Telegram interactions, `boto3` for DynamoDB interactions and for making Yandex Cloud API calls. 

The project structure includes the following key components:
- `main.py`: The entry point for initializing the bot and setting up command handlers.
- `telegram_bot.py`: Contains the core logic for handling incoming messages and commands.
- `utils/`: A directory containing helper modules for managing translations, OpenAI interactions, and database operations.
- `translations.json`: A file for localization, providing translations for user-facing messages in multiple languages.

## Features

1. **User Interaction**: Users can send text messages, photos, audio, and video to the bot, which processes and responds accordingly.
2. **Command Handling**: Supports commands like `/start`, `/help`, `/language`, `/budget`, `/reset`, `/summarize`, `/settings`, and `/users`.
3. **Multilingual Support**: Responds in multiple languages, currently supporting English and Russian.
4. **User Role Management**: Differentiates user roles (owner, admin, user, banned) and provides command sets based on roles.
5. **Budget Management**: Users can view and manage their budget for interactions, with automatic checks before API calls.
6. **Inline Keyboards**: Utilizes inline keyboards for intuitive navigation and command selection.
7. **OpenAI Integration**: Interacts with the OpenAI API to generate responses based on user input.
8. **Database Integration**: User data is stored in a DynamoDB database on Yandex Cloud.
9. **Logging System**: Implements a logging mechanism for tracing application behavior and errors.


### Quickstart

1. Create an account on Yandex Cloud and setup a service account with a static secret key. Create a table for users data in YDB and save the DocumentAPI endpoint of the database.

2. Create an API key in your OpenAI account.

3. Find a working proxy server from any country where OpenAI is available.

4. Create new Yandex Cloud Function with the files from this repository. Fill in the environment variables:
   - `TELEGRAM_BOT_TOKEN`
   - `OWNER_TELEGRAM_ID`
   - `OWNER_TELEGRAM_NAME`
   - `OPENAI_API_KEY`
   - `PROXY`
   - `ACCESS_KEY_ID`
   - `SECRET_ACCESS_KEY`
   - `DOCUMENT_API_ENDPOINT`

5. Setup Yandex Cloud API Gateway with the following configuration:
   ```openapi: 3.0.0
   info:
   title: Sample API
   version: 1.0.0
   servers:
   - url: <gateway_url>
   paths:
   /for-chatgpt-telegram-bot-function:
      post:
         x-yc-apigateway-integration:
         type: cloud_functions
         function_id: <function_id>
         service_account_id: <service_account_id>
         operationId: for-chatgpt-telegram-bot-function```

6. Connect the Telegram bot to the API Gateway (set up the webhook):
  ```python
  import requests

   url = "https://api.telegram.org/bot{token}/{method}".format(
      token="<YOUR_BOT_TOKEN>",
      method = "setWebhook"
      #method="getWebhookinfo"
      #method = "deleteWebhook"
   )

   data = {"url": "<url_from_gateway>/for-chatgpt-telegram-bot-function"}

   r = requests.post(url, data=data)
   print(r.json())
  ```

  7. Start the function in Yandex Cloud Functions and enjoy!

### License

Copyright (c) 2024. All rights reserved.
```