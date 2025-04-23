import re
from config import logger

def sanitize_message(message):
    """
    Sanitize a message to remove any sensitive or harmful content.
    
    Args:
        message (str): The message to sanitize
        
    Returns:
        str: The sanitized message
    """
    # Remove any potentially harmful markdown or HTML
    sanitized = re.sub(r'[<>]', '', message)
    return sanitized.strip()

def create_help_message():
    """Create a help message for the bot."""
    return (
        "🤖 *ChatGPT Telegram Bot Help* 🤖\n\n"
        "This bot connects to OpenAI's ChatGPT to provide AI-powered conversations.\n\n"
        "*Available Commands:*\n"
        "/start - Start a conversation with the bot\n"
        "/help - Show this help message\n"
        "/clear - Clear your conversation history\n\n"
        "*Usage:*\n"
        "- Simply send a message to chat with the AI\n"
        "- The bot remembers your conversation history to maintain context\n"
        "- Use /clear to start a fresh conversation\n\n"
        "*Note:*\n"
        "The bot uses OpenAI's GPT model to generate responses. Your messages are sent to OpenAI for processing."
    )

def create_welcome_message():
    """Create a welcome message for the bot."""
    return (
        "👋 *Welcome to ChatGPT Telegram Bot!* 👋\n\n"
        "I'm powered by OpenAI's GPT model and can have natural conversations with you.\n\n"
        "Simply send me a message to start chatting, and I'll do my best to provide helpful responses.\n\n"
        "Use the /help command to see available options.\n\n"
        "Let's start chatting! What's on your mind today?"
    )

def truncate_message_if_needed(message, max_length=4096):
    """
    Truncate a message if it's too long for Telegram.
    
    Args:
        message (str): The message to check
        max_length (int): Maximum length (Telegram limit is 4096)
        
    Returns:
        str: The possibly truncated message
    """
    if len(message) > max_length:
        return message[:max_length-100] + "\n...\n[Message was truncated as it exceeded Telegram's character limit]"
    return message
