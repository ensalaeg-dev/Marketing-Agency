from crewai import Task
from textwrap import dedent

class MediaTasks:
    """
    Defines the tasks for the Media Management Crew.
    """
    def __init__(self, agents_factory):
        self.agents = agents_factory

    def generate_visual_assets_task(self, post_content: str, platform: str) -> Task:
        return Task(
            description=dedent(f"""
                Review the following post content intended for {platform}:
                ---
                {post_content}
                ---
                Your goal is to generate high-quality visual assets that complement this content.
                
                1. Decide whether an image or a short video is more effective based on the platform norms.
                2. If an image is chosen, use the 'Generate Image with Gemini Imagen' tool or 'DALL-E 3'.
                3. If a video is chosen, use 'Generate Video with Gemini Veo' or 'Runway'.
                4. Ensure the visual style aligns with the Egyptian audience preferences identified by the Intelligence Agent.
                
                Return the URLs of the generated assets.
            """),
            expected_output="A report containing the URLs of the generated image and/or video assets, and a brief explanation of the creative choice.",
            agent=self.agents.media_management_agent()
        )
