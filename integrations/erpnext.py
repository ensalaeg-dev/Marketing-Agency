import os
import requests
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()

class ERPNextIntegration:
    """
    Handles communication with the ERPNext API for marketing automation.
    Requires ERPNEXT_URL, ERPNEXT_API_KEY, and ERPNEXT_API_SECRET in the environment.
    """
    
    def __init__(self):
        self.base_url = os.getenv("ERPNEXT_URL", "").rstrip("/")
        self.api_key = os.getenv("ERPNEXT_API_KEY")
        self.api_secret = os.getenv("ERPNEXT_API_SECRET")
        
        if not self.base_url or not self.api_key or not self.api_secret:
            raise ValueError("ERPNext environment variables (URL, API_KEY, API_SECRET) are missing.")
            
        self.headers = {
            "Authorization": f"token {self.api_key}:{self.api_secret}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Helper to make GET requests to ERPNext API."""
        url = f"{self.base_url}/api/resource/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_active_campaigns(self) -> List[Dict[str, Any]]:
        """
        Retrieves active marketing campaigns from ERPNext.
        Assuming a Doctype named 'Campaign' exists.
        """
        params = {
            "filters": '[["name","!=",""]]', # Replace with actual status filters like [["status","=","Active"]]
            "fields": '["name", "campaign_name", "description"]',
            "limit_page_length": 50
        }
        try:
            data = self._get("Campaign", params=params)
            return data.get("data", [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching campaigns: {e}")
            return []

    def get_products(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieves products from ERPNext (Item Doctype).
        """
        filters = []
        if category:
            filters.append(f'["item_group", "=", "{category}"]')
        
        filter_str = f"[{','.join(filters)}]" if filters else None
        
        params = {
            "fields": '["name", "item_name", "description", "standard_rate", "item_group"]',
            "limit_page_length": 100
        }
        if filter_str:
            params["filters"] = filter_str

        try:
            data = self._get("Item", params=params)
            return data.get("data", [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching products: {e}")
            return []
            
    def get_business_info(self) -> Dict[str, Any]:
        """
        Retrieves company information.
        """
        params = {
            "fields": '["name", "company_name", "domain", "email"]',
            "limit_page_length": 1
        }
        try:
            data = self._get("Company", params=params)
            companies = data.get("data", [])
            return companies[0] if companies else {}
        except requests.exceptions.RequestException as e:
            print(f"Error fetching company info: {e}")
            return {}

if __name__ == "__main__":
    # Example usage
    # Ensure you have your .env filled before running this directly
    try:
        erp = ERPNextIntegration()
        print("Active Campaigns:", erp.get_active_campaigns())
    except ValueError as e:
        print(e)
