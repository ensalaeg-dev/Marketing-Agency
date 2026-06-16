from langchain.tools import tool
from integrations.erpnext import ERPNextIntegration
from community_database.models import init_db, Community, Campaign, Post
import os

db_url = os.getenv("DATABASE_URL", "sqlite:///growth_specialist.db")
Session = init_db(db_url)

@tool("Fetch Active ERPNext Campaigns")
def fetch_erpnext_campaigns(query: str) -> str:
    """
    Fetches currently active marketing campaigns from ERPNext.
    The query parameter is ignored but required by Langchain.
    Returns a string representation of the active campaigns.
    """
    try:
        erp = ERPNextIntegration()
        campaigns = erp.get_active_campaigns()
        if not campaigns:
            return "No active campaigns found in ERPNext."
        
        result = "Active Campaigns:\n"
        for c in campaigns:
            result += f"- {c.get('campaign_name', c.get('name'))}: {c.get('description', 'No description')}\n"
        return result
    except Exception as e:
        return f"Error fetching campaigns from ERPNext: {str(e)}"

@tool("Fetch ERPNext Products")
def fetch_erpnext_products(category: str = "") -> str:
    """
    Fetches products from ERPNext. 
    Optionally pass a category (item_group) to filter products.
    """
    try:
        erp = ERPNextIntegration()
        products = erp.get_products(category=category if category else None)
        if not products:
            return "No products found."
        
        result = "Products:\n"
        for p in products[:10]: # Limit to 10 for context window safety
            result += f"- {p.get('item_name', p.get('name'))} (Category: {p.get('item_group', 'None')}): {p.get('standard_rate', 'N/A')} EGP\n"
        return result
    except Exception as e:
        return f"Error fetching products from ERPNext: {str(e)}"

@tool("Save Discovered Community")
def save_discovered_community(data: str) -> str:
    """
    Saves a newly discovered Egyptian community to the database.
    The data should be a JSON string with keys: name, platform, url, governorate, audience_size, main_topics.
    """
    import json
    try:
        community_data = json.loads(data)
        
        # Simple check if URL already exists
        existing = Session.query(Community).filter_by(url=community_data.get("url")).first()
        if existing:
            return f"Community with URL {community_data.get('url')} already exists in the database."
            
        new_community = Community(
            name=community_data.get("name"),
            platform=community_data.get("platform"),
            url=community_data.get("url"),
            governorate=community_data.get("governorate", "All"),
            audience_size=community_data.get("audience_size", 0),
            main_topics=community_data.get("main_topics", ""),
            status="Needs Review"
        )
        Session.add(new_community)
        Session.commit()
        return f"Successfully saved community: {new_community.name}"
    except Exception as e:
        Session.rollback()
        return f"Error saving community: {str(e)}"

@tool("Save Draft Post")
def save_draft_post(data: str) -> str:
    """
    Saves a drafted content post to the database for human approval.
    Data should be a JSON string with keys: content, language, community_url.
    """
    import json
    try:
        post_data = json.loads(data)
        
        # Find community ID
        community = Session.query(Community).filter_by(url=post_data.get("community_url")).first()
        community_id = community.id if community else None
        
        new_post = Post(
            content=post_data.get("content"),
            language=post_data.get("language", "Egyptian Arabic"),
            community_id=community_id,
            status="Needs Approval"
        )
        Session.add(new_post)
        Session.commit()
        return f"Successfully drafted post. Pending human approval."
    except Exception as e:
        Session.rollback()
        return f"Error saving draft post: {str(e)}"
