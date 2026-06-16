import requests
from crewai_tools import BaseTool
from pydantic import Field
from typing import Any

class SearXNGSearchTool(BaseTool):
    name: str = "SearXNG Search"
    description: str = "A tool to search the internet using a self-hosted SearXNG instance. Useful for finding Egyptian communities, forums, and local websites."
    base_url: str = Field(default="http://localhost:8080", description="The base URL of the SearXNG instance")

    def _run(self, query: str) -> str:
        """
        Executes a search query against the SearXNG instance.
        """
        search_url = f"{self.base_url}/search"
        params = {
            "q": query,
            "format": "json",
            "engines": "google,bing,duckduckgo",
            "language": "ar-EG" # Focus on Egyptian Arabic/Egypt results
        }
        
        try:
            response = requests.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            results = response.json().get("results", [])
            
            if not results:
                return f"No results found for query: {query}"
            
            # Format top 5 results for the agent
            formatted_results = []
            for res in results[:5]:
                formatted_results.append(f"Title: {res.get('title')}\nURL: {res.get('url')}\nSnippet: {res.get('content')}\n")
            
            return "\n---\n".join(formatted_results)
            
        except Exception as e:
            return f"Error connecting to SearXNG at {self.base_url}: {str(e)}. Ensure SearXNG is running via Docker."
