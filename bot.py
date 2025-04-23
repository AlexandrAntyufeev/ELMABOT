import time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai_client import OpenAIClient
from conversation_handler import ConversationHandler
from utils import sanitize_message, create_help_message, create_welcome_message, truncate_message_if_needed
from config import TELEGRAM_BOT_TOKEN, logger

class TelegramBot:
    def __init__(self):
        """Initialize the Telegram bot with handlers."""
        if not TELEGRAM_BOT_TOKEN:
            raise ValueError("Telegram bot token not found. Please set the TELEGRAM_BOT_TOKEN environment variable.")
        
        # Initialize the OpenAI client and conversation handler
        self.openai_client = OpenAIClient()
        self.conversation_handler = ConversationHandler()
        
        # Create the Application
        self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        # Add handlers
        self._add_handlers()
        
        logger.info("Telegram bot initialized")
    
    def _add_handlers(self):
        """Add command and message handlers to the application."""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("clear", self.clear_command))
        
        # Message handler for text messages
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Error handler
        self.application.add_error_handler(self.error_handler)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command."""
        logger.info(f"User {update.effective_user.id} started the bot")
        
        welcome_message = create_welcome_message()
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /help command."""
        logger.info(f"User {update.effective_user.id} requested help")
        
        help_message = create_help_message()
        await update.message.reply_text(help_message, parse_mode='Markdown')
    
    async def clear_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /clear command to clear conversation history."""
        user_id = update.effective_user.id
        logger.info(f"User {user_id} cleared their conversation history")
        
        if self.conversation_handler.clear_conversation(user_id):
            await update.message.reply_text("Your conversation history has been cleared. Let's start fresh!")
        else:
            await update.message.reply_text("Sorry, there was an error clearing your conversation history.")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages from users."""
        user_id = update.effective_user.id
        message_text = update.message.text
        
        # Подробное логирование входящего сообщения
        logger.info(f"Received message from user {user_id}: \"{message_text}\"")
        logger.info(f"User info: {update.effective_user.first_name} (@{update.effective_user.username})")
        
        try:
            # Notify user that the bot is "typing"
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            
            # Sanitize the input message
            sanitized_message = sanitize_message(message_text)
            logger.info(f"Sanitized message: \"{sanitized_message}\"")
            
            # Add user message to conversation history
            self.conversation_handler.add_message(user_id, "user", sanitized_message)
            
            # Get the entire conversation history
            conversation = self.conversation_handler.get_conversation(user_id)
            logger.info(f"Conversation history contains {len(conversation)} messages")
            
            # Get response from OpenAI
            logger.info("Sending request to OpenAI...")
            start_time = time.time()
            response = self.openai_client.get_response(conversation)
            elapsed_time = time.time() - start_time
            logger.info(f"OpenAI response received in {elapsed_time:.2f} seconds: \"{response[:50]}...\"")
            
            # Add assistant response to conversation history
            self.conversation_handler.add_message(user_id, "assistant", response)
            
            # Ensure the response isn't too long for Telegram
            response = truncate_message_if_needed(response)
            
            # Send the response
            logger.info("Sending response to user...")
            await update.message.reply_text(response)
            logger.info("Response sent successfully!")
        except Exception as e:
            logger.error(f"Error handling message: {e}", exc_info=True)
            try:
                await update.message.reply_text("Произошла ошибка при обработке вашего сообщения. Пожалуйста, попробуйте еще раз позже.")
            except Exception as send_error:
                logger.error(f"Failed to send error message: {send_error}")
    
    async def error_handler(self, update, context):
        """Handle errors in the telegram-python-bot library."""
        logger.error(f"Update {update} caused error: {context.error}")
        
        # Notify user of error
        if update and update.effective_chat:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sorry, something went wrong while processing your request. Please try again later."
            )
    
    def run(self):
        """Run the bot until the user presses Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT."""
        logger.info("Starting bot polling...")
        self.application.run_polling()
        
    async def run_async(self):
        """Run the bot asynchronously."""
        logger.info("Starting bot polling asynchronously...")
        
        # В версии python-telegram-bot 22.0 следует использовать этот метод
        # для асинхронного запуска бота
        await self.application.initialize()
        await self.application.start()
