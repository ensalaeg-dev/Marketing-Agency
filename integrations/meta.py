import os
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class MetaIntegration:
    """
    Handles communication with Meta Graph API for Facebook and Instagram publishing.
    """
    
    def __init__(self):
        self.access_token = os.getenv("META_ACCESS_TOKEN")
        self.graph_version = "v19.0"
        self.base_url = f"https://graph.facebook.com/{self.graph_version}"
        
        if not self.access_token:
            raise ValueError("META_ACCESS_TOKEN is missing in environment variables.")

    def publish_post(self, page_id: str, message: str, link: Optional[str] = None) -> Dict[str, Any]:
        """
        Publishes a text or link post to a Facebook Page.
        """
        url = f"{self.base_url}/{page_id}/feed"
        payload = {
            "message": message,
            "access_token": self.access_token
        }
        if link:
            payload["link"] = link
            
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error publishing to Meta (Page ID: {page_id}): {e}")
            if e.response is not None:
                print(e.response.json())
            return {}

    def get_page_insights(self, page_id: str, metric: str = "page_impressions,page_engaged_users") -> Dict[str, Any]:
        """
        Retrieves insights for a specific page.
        """
        url = f"{self.base_url}/{page_id}/insights"
        params = {
            "metric": metric,
            "period": "day",
            "access_token": self.access_token
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Meta insights: {e}")
            return {}
