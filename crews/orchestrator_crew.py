from crewai import Crew, Process, Task
from agents.platform_teams import PlatformTeams
from agents.core_agents import get_llm
from textwrap import dedent

class HierarchicalOrchestrator:
    """
    The Master Orchestrator that spawns and manages platform-specific 'Teams of Teams'.
    """

    def __init__(self):
        # The Manager LLM needs to be highly capable (e.g., GPT-4 or Gemini 1.5 Pro)
        self.manager_llm = get_llm("Orchestrator Manager")
        self.teams = PlatformTeams()

    def run_omnichannel_campaign(self, campaign_objective: str):
        # 1. Build all platform teams
        fb_team = self.teams.build_facebook_team()
        wa_team = self.teams.build_whatsapp_team()
        tg_team = self.teams.build_telegram_team()
        forum_team = self.teams.build_forums_team()
        media_team = self.teams.build_media_team()
        
        # 2. Collect all agents into a pool
        all_agents = fb_team + wa_team + tg_team + forum_team + media_team
        
        # 3. Define the High-Level Orchestration Tasks
        # The Manager will delegate the 'how' to the platform teams.
        distribute_campaign_task = Task(
            description=dedent(f"""
                Objective: {campaign_objective}
                
                Your goal as the Manager is to coordinate an omnichannel marketing campaign across:
                1. Facebook (Strategy & Copy)
                2. WhatsApp (Direct Messaging)
                3. Telegram (Channel Growth)
                4. General Egyptian Web Forums (Engagement)
                
                You must:
                - Delegate discovery tasks to each platform's researcher.
                - Delegate content creation to each platform's writer.
                - Coordinate with the Media Director to ensure high-quality visual assets (images/video) are created.
                - Ensure all content uses authentic Egyptian Arabic (Amiya).
                - Save all drafted posts and discovered communities to the database using the provided tools.
            """),
            expected_output="A full report on the execution across all platforms, including links to drafted posts and saved communities.",
        )

        # 4. Create the Hierarchical Crew
        crew = Crew(
            agents=all_agents,
            tasks=[distribute_campaign_task],
            process=Process.hierarchical,
            manager_llm=self.manager_llm,
            verbose=True
        )
        
        print(f"--- Launching Omnichannel Orchestrator for: {campaign_objective} ---")
        result = crew.kickoff()
        return result
