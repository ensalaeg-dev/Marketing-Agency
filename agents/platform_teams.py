from crewai import Agent
from agents.core_agents import get_llm, search_tool
from tools.custom_tools import save_discovered_community, save_draft_post, fetch_erpnext_campaigns, fetch_erpnext_products
from tools.media_tools import MediaGenerationTools

class PlatformTeams:
    """
    Factory class to build isolated teams of agents for each platform.
    """

    @staticmethod
    def build_facebook_team():
        return [
            Agent(
                role="Facebook Market Strategist",
                goal="Analyze Facebook groups and pages in Egypt to identify viral trends and community rules.",
                backstory="An expert in the Egyptian Facebook ecosystem. You know the difference between 'Sale' groups in Cairo and community groups in Delta.",
                llm=get_llm("Facebook Strategist"),
                tools=[search_tool, save_discovered_community]
            ),
            Agent(
                role="Facebook Content Copywriter",
                goal="Write highly engaging Facebook posts in Egyptian Arabic (Amiya).",
                backstory="A social media native who knows how to use emojis, hashtags, and Egyptian slang to get maximum reach on Facebook.",
                llm=get_llm("Facebook Copywriter"),
                tools=[save_draft_post]
            )
        ]

    @staticmethod
    def build_whatsapp_team():
        return [
            Agent(
                role="WhatsApp Community Manager",
                goal="Discover and manage Egyptian WhatsApp communities and channels for targeted marketing.",
                backstory="You are a master of WhatsApp marketing. You know how to find invite links and engage with users in private communities.",
                llm=get_llm("WhatsApp Manager"),
                tools=[search_tool, save_discovered_community]
            ),
            Agent(
                role="WhatsApp Promotional Writer",
                goal="Draft persuasive, short-form messages for WhatsApp communities in Egyptian Arabic.",
                backstory="You specialize in the 'WhatsApp hook'—messages that people actually open and reply to.",
                llm=get_llm("WhatsApp Writer"),
                tools=[save_draft_post]
            )
        ]

    @staticmethod
    def build_telegram_team():
        return [
            Agent(
                role="Telegram Channel Specialist",
                goal="Discover Egyptian Telegram channels and groups related to business and retail.",
                backstory="You understand the Egyptian Telegram landscape, focusing on price-comparison channels and wholesale groups.",
                llm=get_llm("Telegram Specialist"),
                tools=[search_tool, save_discovered_community]
            ),
            Agent(
                role="Telegram Content Creator",
                goal="Draft posts for Telegram channels that drive clicks and sales.",
                backstory="A specialist in Telegram's long-form and link-heavy posting style.",
                llm=get_llm("Telegram Writer"),
                tools=[save_draft_post]
            )
        ]

    @staticmethod
    def build_forums_team():
        return [
            Agent(
                role="Egyptian Forum Researcher",
                goal="Search for niche Egyptian web forums and community sites for industry-specific discussions.",
                backstory="An expert in finding old-school and niche Egyptian forums where high-intent discussions happen.",
                llm=get_llm("Forum Researcher"),
                tools=[search_tool, save_discovered_community]
            ),
            Agent(
                role="Forum Engagement Specialist",
                goal="Draft high-value, helpful forum posts that subtly promote the brand.",
                backstory="You are a master of 'helpful marketing.' You provide tips first and products second.",
                llm=get_llm("Forum Writer"),
                tools=[save_draft_post]
            )
        ]

    @staticmethod
    def build_media_team():
        # The media team supports all platforms
        return [
            Agent(
                role="Egyptian Creative Director",
                goal="Generate high-quality visual assets tailored for the Egyptian market across all platforms using Nano Banana and Veo.",
                backstory="A visionary director who understands what visuals resonate in Egypt. "
                          "Equipped with Google Nano Banana and Veo for next-generation image and video generation.",
                llm=get_llm("Media Director"),
                tools=[
                    MediaGenerationTools.generate_image_nano_banana,
                    MediaGenerationTools.generate_video_veo,
                    MediaGenerationTools.generate_image_dalle,
                    MediaGenerationTools.generate_video_runway
                ]
            )
        ]
