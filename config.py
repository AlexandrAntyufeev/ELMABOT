import os
import logging

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    logger.error("No TELEGRAM_BOT_TOKEN found in environment variables!")

# OpenAI configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("No OPENAI_API_KEY found in environment variables!")

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_MODEL = "gpt-4o"

# Maximum conversation history length
MAX_HISTORY_LENGTH = 10

# Default system message for ChatGPT
DEFAULT_SYSTEM_MESSAGE = "You are a helpful assistant integrated into a Telegram bot. Provide concise, accurate and helpful responses."
