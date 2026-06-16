import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class TelegramIntegration:
    """
    Handles communication with Telegram Bot API.
    """
    
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN is missing in environment variables.")
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    def send_message(self, chat_id: str, text: str) -> Dict[str, Any]:
        """
        Sends a message to a specific Telegram chat (Channel or Group).
        """
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending Telegram message: {e}")
            if e.response is not None:
                print(e.response.json())
            return {}
