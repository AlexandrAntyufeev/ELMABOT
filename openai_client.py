import os
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL, logger, DEFAULT_SYSTEM_MESSAGE

class OpenAIClient:
    def __init__(self):
        """Initialize the OpenAI client with API key."""
        if not OPENAI_API_KEY:
            logger.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
            raise ValueError("OpenAI API key not found")
            
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.model = OPENAI_MODEL
        self.system_message = DEFAULT_SYSTEM_MESSAGE
        
    def get_response(self, messages):
        """
        Get a response from the OpenAI API.
        
        Args:
            messages (list): List of message dictionaries with role and content keys.
            
        Returns:
            str: The response text
        """
        try:
            # Ensure the system message is the first in the list
            if messages and messages[0].get("role") != "system":
                messages = [{"role": "system", "content": self.system_message}] + messages
                
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error getting response from OpenAI: {e}")
            return f"Sorry, I encountered an error while processing your request: {str(e)}"
    
    def change_system_message(self, new_system_message):
        """
        Change the system message that guides the AI's behavior.
        
        Args:
            new_system_message (str): The new system message
            
        Returns:
            bool: True if successful
        """
        try:
            self.system_message = new_system_message
            return True
        except Exception as e:
            logger.error(f"Error changing system message: {e}")
            return False
