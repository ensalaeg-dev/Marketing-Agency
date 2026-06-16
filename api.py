from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crews.discovery_crew import DiscoveryCrew
from crews.content_crew import ContentCrew
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Egyptian Growth Specialist API")

class DiscoveryRequest(BaseModel):
    topic: str
    platform: str

class ContentRequest(BaseModel):
    governorate: str
    community_url: str

@app.get("/")
def read_root():
    return {"status": "online", "message": "Egyptian Omnichannel Growth Specialist API"}

@app.post("/api/discover")
async def run_discovery(request: DiscoveryRequest):
    try:
        crew = DiscoveryCrew()
        result = crew.run(target_topic=request.topic, platform_focus=request.platform)
        return {"status": "success", "result": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate")
async def run_content_engine(request: ContentRequest):
    try:
        crew = ContentCrew()
        result = crew.run(governorate_focus=request.governorate, community_url=request.community_url)
        return {"status": "success", "result": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
