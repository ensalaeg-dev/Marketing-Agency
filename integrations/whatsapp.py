import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class WhatsAppIntegration:
    """
    Handles communication with WhatsApp Cloud API for Business.
    """
    
    def __init__(self):
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        self.bearer_token = os.getenv("WHATSAPP_BEARER_TOKEN")
        self.graph_version = "v19.0"
        self.base_url = f"https://graph.facebook.com/{self.graph_version}"
        
        if not self.phone_number_id or not self.bearer_token:
            raise ValueError("WhatsApp credentials are missing in environment variables.")
            
        self.headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json"
        }

    def send_template_message(self, to_phone_number: str, template_name: str, language_code: str = "ar") -> Dict[str, Any]:
        """
        Sends an approved template message to a user.
        """
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending WhatsApp message: {e}")
            if e.response is not None:
                print(e.response.json())
            return {}
