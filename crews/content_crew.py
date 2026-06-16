from crewai import Crew, Process
from agents.core_agents import EgyptianGrowthAgents
from tasks.content_tasks import ContentTasks

class ContentCrew:
    def __init__(self):
        self.agents = EgyptianGrowthAgents()
        self.tasks = ContentTasks(self.agents)

    def run(self, governorate_focus: str, community_url: str):
        # Instantiate agents
        erp_agent = self.agents.erpnext_integration_agent()
        audience_agent = self.agents.egyptian_audience_intelligence_agent()
        content_agent = self.agents.content_creation_agent()
        
        # Instantiate tasks
        fetch_data_task = self.tasks.fetch_campaign_data_task()
        analyze_task = self.tasks.analyze_audience_task(governorate_focus)
        generate_post_task = self.tasks.generate_localized_content_task(community_url)
        
        # Create Crew
        crew = Crew(
            agents=[erp_agent, audience_agent, content_agent],
            tasks=[fetch_data_task, analyze_task, generate_post_task],
            process=Process.sequential,
            verbose=True
        )
        
        print(f"Starting Content Engine Crew for community '{community_url}'...")
        result = crew.kickoff()
        return result
