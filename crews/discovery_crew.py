from crewai import Crew, Process
from agents.core_agents import EgyptianGrowthAgents
from tasks.discovery_tasks import DiscoveryTasks

class DiscoveryCrew:
    def __init__(self):
        self.agents = EgyptianGrowthAgents()
        self.tasks = DiscoveryTasks(self.agents)

    def run(self, target_topic: str, platform_focus: str):
        # Instantiate agents
        discovery_agent = self.agents.community_discovery_agent()
        
        # Instantiate tasks
        search_task = self.tasks.search_for_communities_task(target_topic, platform_focus)
        
        # Create Crew
        crew = Crew(
            agents=[discovery_agent],
            tasks=[search_task],
            process=Process.sequential,
            verbose=True
        )
        
        print(f"Starting Discovery Crew for topic '{target_topic}' on '{platform_focus}'...")
        result = crew.kickoff()
        return result
