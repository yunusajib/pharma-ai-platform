from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv
import time

from agents.orchestrator import AgentOrchestrator

load_dotenv()

app = FastAPI(
    title="Pharma AI Backend",
    version="1.0.0"
)

orchestrator = AgentOrchestrator()

class QueryRequest(BaseModel):
    query: str
    user_id: str
    hcp_context: Optional[dict] = None

class ComplianceCheck(BaseModel):
    status: str
    violation_type: Optional[str] = None
    explanation: Optional[str] = None

class QueryResponse(BaseModel):
    query: str
    response: str
    agents_used: List[str]
    compliance_status: ComplianceCheck
    response_time_seconds: float

@app.get("/")
def read_root():
    return {
        "message": "Pharma AI Backend",
        "status": "operational",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "timestamp": time.time()
    }

@app.post("/api/query")
async def process_query(request: QueryRequest):
    try:
        result = await orchestrator.process_query(
            query=request.query,
            user_id=request.user_id,
            hcp_context=request.hcp_context
        )
        
        return {
            "query": request.query,
            "response": result["response"],
            "agents_used": result["agents_used"],
            "compliance_status": result["compliance_status"],
            "response_time_seconds": result["response_time_seconds"]
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/agents/status")
def get_agent_status():
    openai_configured = bool(os.getenv("OPENAI_API_KEY"))
    return {
        "total_agents": 5,
        "agents": [
            {"name": "sales_agent", "status": "active" if openai_configured else "offline", "version": "1.0.0"},
            {"name": "compliance_guardian", "status": "active", "version": "1.0.0"},
        ],
        "system_status": "operational",
        "openai_configured": openai_configured
    }

@app.on_event("startup")
async def startup_event():
    print("🚀 Backend starting...")
    print("✅ OpenAI:", "configured" if os.getenv("OPENAI_API_KEY") else "NOT SET")
    print("✅ Ready!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
