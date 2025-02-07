# Telegram Bot with Secure Environment Variable Management

## Overview
This Python script is a Telegram bot that securely loads environment variables from an encrypted `.env.enc` file. The bot provides an administrative `/shutdown` command that sends a POST request to a specific URL. Only authorized users (as defined by `ADMIN_ID`) can execute the shutdown command.

## Features
- **Secure Environment Variables**: Uses Fernet encryption to decrypt `.env.enc` without writing to disk.
- **Telegram Bot Integration**: Uses `pyTelegramBotAPI` (Telebot) to interact with Telegram.
- **Command Execution**: Provides a `/shutdown` command to trigger a remote API.
- **Logging**: Logs critical actions and errors.

## Requirements
- Python 3.x
- `requests` library
- `pyTelegramBotAPI` library
- `cryptography` library

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repository.git
    cd your-repository
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Run the bot:
    ```bash
    python moneymanafrica_bot.py
    ```

## Configuration
### Environment Variables
Your `.env` file should contain:
```
only the `.env.enc` file is used by the bot.

## Usage
1. Start the bot.
2. Use `/start` to verify the bot is active.
3. Use `/shutdown` (admin only) to send a shutdown request.

## Security Considerations
- Do not hardcode sensitive credentials in the script.
- Store and manage the encryption key securely.
- Restrict access to `.env.enc`.

## License
This project is under [MIT License](LICENSE).

