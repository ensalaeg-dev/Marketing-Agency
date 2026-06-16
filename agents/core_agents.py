import os
import json
from crewai import Agent
from tools.searxng_tool import SearXNGSearchTool
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.custom_tools import fetch_erpnext_campaigns, fetch_erpnext_products, save_discovered_community, save_draft_post
from tools.media_tools import MediaGenerationTools

def get_llm(agent_name: str):
    """
    Dynamically loads the LLM based on agent_models.json configuration.
    """
    # Defaults
    provider = "openai"
    model = "gpt-4-turbo"
    
    config_file = "agent_models.json"
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            try:
                config = json.load(f)
                if agent_name in config:
                    provider = config[agent_name].get("provider", provider).lower()
                    model = config[agent_name].get("model", model)
            except Exception as e:
                print(f"Error loading agent_models.json: {e}. Falling back to defaults.")

    if provider == "gemini":
        return ChatGoogleGenerativeAI(
            model=model,
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.7
        )
    
    # Generic API handling (OpenAI, Kimi, Anthropic, Mistral) via ChatOpenAI interface
    api_key = os.getenv(f"{provider.upper()}_API_KEY")
    if not api_key and provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        
    base_url = None
    if provider == "kimi":
        base_url = os.getenv("KIMI_BASE_URL", "https://api.moonshot.cn/v1")
    elif provider == "mistral":
        base_url = "https://api.mistral.ai/v1"
    elif provider == "anthropic":
        # Anthropic has a slightly different schema, but LiteLLM or Langchain usually handles it.
        # For this implementation, we assume OpenAI-compatible routing or specific provider logic.
        pass
        
    return ChatOpenAI(
        model_name=model,
        api_key=api_key,
        base_url=base_url,
        temperature=0.7
    )

# Search tool for discovery (Self-hosted SearXNG)
search_tool = SearXNGSearchTool()

class EgyptianGrowthAgents:
    """
    Defines the 8 core CrewAI agents for the Egyptian Omnichannel Community Growth Specialist.
    """

    def community_discovery_agent(self) -> Agent:
        return Agent(
            role="Community Discovery Specialist",
            goal="Discover, catalog, and evaluate Egyptian online communities across Meta, WhatsApp, Telegram, and Forums.",
            backstory="An expert OSINT researcher embedded in the Egyptian digital landscape. "
                      "You know how to find the most active Facebook groups in Alexandria, "
                      "the most engaged WhatsApp communities for wholesale buyers in Cairo, and niche Telegram channels.",
            verbose=True,
            allow_delegation=False,
            llm=get_llm("Discovery Specialist"),
            tools=[search_tool, save_discovered_community]
        )

    def egyptian_audience_intelligence_agent(self) -> Agent:
        return Agent(
            role="Egyptian Audience Intelligence Analyst",
            goal="Analyze and map out Egyptian audience behaviors, governorate differences, and cultural nuances.",
            backstory="A cultural anthropologist and market researcher. You understand the difference in buying power "
                      "between Zamalek and Nasr City, the impact of Ramadan on purchasing, and how to speak "
                      "in authentic 'Amiya Masriya' (Egyptian Arabic) without sounding forced.",
            verbose=True,
            allow_delegation=True,
            llm=get_llm("Audience Intelligence")
        )

    def erpnext_integration_agent(self) -> Agent:
        return Agent(
            role="ERPNext Data Controller",
            goal="Securely extract product, campaign, and business data from the ERPNext backend.",
            backstory="A precise and highly secure data engineer who acts as the bridge between the company's "
                      "ERPNext system and the marketing engine. You ensure all AI agents have accurate, up-to-date "
                      "inventory and pricing information.",
            verbose=True,
            allow_delegation=False,
            llm=get_llm("ERPNext Controller"),
            tools=[fetch_erpnext_campaigns, fetch_erpnext_products]
        )

    def content_creation_agent(self) -> Agent:
        return Agent(
            role="Egyptian Omnichannel Copywriter",
            goal="Generate engaging, culturally resonant content tailored to specific Egyptian communities and platforms.",
            backstory="A witty Egyptian social media manager who knows exactly what makes a post go viral on Facebook "
                      "versus what drives sales in a B2B Telegram channel. You are a master of Egyptian street slang, "
                      "formal Arabic, and persuasive copy.",
            verbose=True,
            allow_delegation=False,
            llm=get_llm("Content Copywriter"),
            tools=[save_draft_post]
        )

    def media_management_agent(self) -> Agent:
        return Agent(
            role="Media & Creative Director",
            goal="Suggest the optimal media format and generate high-quality visual assets using AI models like Gemini Veo/Imagen or Runway.",
            backstory="A visionary art director with a deep understanding of what visually appeals to the Egyptian market. "
                      "You are equipped with tools to generate images and videos on demand using Gemini Imagen, Veo, Runway, and DALL-E.",
            verbose=True,
            allow_delegation=False,
            llm=get_llm("Media Director"),
            tools=[
                MediaGenerationTools.generate_image_gemini,
                MediaGenerationTools.generate_video_gemini,
                MediaGenerationTools.generate_image_dalle,
                MediaGenerationTools.generate_video_runway,
                MediaGenerationTools.generate_with_replicate,
                MediaGenerationTools.generate_image_stability
            ]
        )

    def publishing_agent(self) -> Agent:
        return Agent(
            role="Omnichannel Publisher",
            goal="Coordinate the actual distribution of approved content to Meta, WhatsApp, and Telegram.",
            backstory="A meticulous traffic controller. You ensure that posts go out at the peak times for Egyptian audiences.",
            verbose=True,
            allow_delegation=False,
            llm=get_llm("Publisher")
        )

    def community_interaction_agent(self) -> Agent:
        return Agent(
            role="Community Manager & Moderator",
            goal="Monitor engagement, suggest replies to comments, and escalate sensitive issues.",
            backstory="The friendly face of the brand. You respond with speed and politeness in local dialect.",
            verbose=True,
            allow_delegation=True,
            llm=get_llm("Interaction Manager")
        )

    def analytics_agent(self) -> Agent:
        return Agent(
            role="Growth & Analytics Specialist",
            goal="Track campaign performance, conversion metrics, and community growth to generate optimization reports.",
            backstory="A data-driven marketer who loves numbers.",
            verbose=True,
            allow_delegation=False,
            llm=get_llm("Analytics Specialist")
        )
