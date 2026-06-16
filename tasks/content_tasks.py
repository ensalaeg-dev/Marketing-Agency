from crewai import Task
from textwrap import dedent

class ContentTasks:
    """
    Defines the tasks for the Content Engine Crew.
    """
    def __init__(self, agents_factory):
        self.agents = agents_factory

    def fetch_campaign_data_task(self) -> Task:
        return Task(
            description=dedent("""
                Use the 'Fetch Active ERPNext Campaigns' tool to see what marketing campaigns are currently running.
                Then, use the 'Fetch ERPNext Products' tool to gather details on the products you need to promote.
                Compile a brief summary of the campaign goals and the products to be promoted.
            """),
            expected_output="A structured summary of active campaigns and target products to be used by the copywriting team.",
            agent=self.agents.erpnext_integration_agent()
        )

    def analyze_audience_task(self, governorate_focus: str) -> Task:
        return Task(
            description=dedent(f"""
                Analyze the audience for the governorate: '{governorate_focus}'.
                Provide insights on cultural nuances, purchasing behavior, and the best tone of voice 
                (e.g., Amiya Masriya) to use when selling products to this demographic.
            """),
            expected_output="A brief demographic and cultural profile detailing the best tone of voice and cultural hooks to use.",
            agent=self.agents.egyptian_audience_intelligence_agent()
        )

    def generate_localized_content_task(self, community_url: str) -> Task:
        return Task(
            description=dedent(f"""
                Using the product summary and the audience analysis provided by previous tasks, 
                draft a highly engaging, localized social media post meant to be published 
                on the community at: {community_url}
                
                The post must:
                1. Use authentic Egyptian Arabic (Amiya).
                2. Be persuasive and include a clear Call To Action.
                3. Adhere to the tone recommended by the Audience Intelligence Agent.
                
                Once drafted, use the 'Save Draft Post' tool to save it to the database for human approval.
                Pass the JSON payload correctly to the tool with keys: content, language, community_url.
            """),
            expected_output="Confirmation that the localized post has been drafted and saved to the database.",
            agent=self.agents.content_creation_agent()
        )
