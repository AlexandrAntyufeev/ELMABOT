from config import MAX_HISTORY_LENGTH, logger

class ConversationHandler:
    def __init__(self):
        """Initialize conversation history storage."""
        # Dictionary to store conversation history per user
        self.conversations = {}
        
    def add_message(self, user_id, role, content):
        """
        Add a message to a user's conversation history.
        
        Args:
            user_id (int): Telegram user ID
            role (str): Message role ('user' or 'assistant')
            content (str): Message content
            
        Returns:
            list: Updated conversation history
        """
        if user_id not in self.conversations:
            self.conversations[user_id] = []
            
        # Add the new message
        self.conversations[user_id].append({"role": role, "content": content})
        
        # Trim the conversation if it exceeds the maximum length
        # Keep the most recent messages
        if len(self.conversations[user_id]) > MAX_HISTORY_LENGTH:
            self.conversations[user_id] = self.conversations[user_id][-MAX_HISTORY_LENGTH:]
            
        return self.conversations[user_id]
    
    def get_conversation(self, user_id):
        """
        Get a user's conversation history.
        
        Args:
            user_id (int): Telegram user ID
            
        Returns:
            list: Conversation history for the user
        """
        if user_id not in self.conversations:
            self.conversations[user_id] = []
            
        return self.conversations[user_id]
    
    def clear_conversation(self, user_id):
        """
        Clear a user's conversation history.
        
        Args:
            user_id (int): Telegram user ID
            
        Returns:
            bool: True if successful
        """
        try:
            self.conversations[user_id] = []
            return True
        except Exception as e:
            logger.error(f"Error clearing conversation: {e}")
            return False
