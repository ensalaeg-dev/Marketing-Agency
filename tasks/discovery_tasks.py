from crewai import Task
from textwrap import dedent

class DiscoveryTasks:
    """
    Defines the tasks for the Community Discovery Crew.
    """
    def __init__(self, agents_factory):
        self.agents = agents_factory

    def search_for_communities_task(self, target_topic: str, platform_focus: str) -> Task:
        return Task(
            description=dedent(f"""
                Search the internet to identify 5 high-potential online communities 
                in Egypt related to the topic: '{target_topic}'.
                Focus primarily on the platform: '{platform_focus}'.
                
                For each community, you must gather:
                - Name
                - Platform
                - URL
                - Estimated Audience Size
                - Relevance to specific governorates (if any)
                - Main sub-topics discussed
                
                Use the 'Save Discovered Community' tool to log each of these 5 communities into the database.
            """),
            expected_output="A list of the 5 communities found and a confirmation that they were saved to the database.",
            agent=self.agents.community_discovery_agent()
        )
