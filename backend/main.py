from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv
import time

from agents.orchestrator import AgentOrchestrator

load_dotenv()

app = FastAPI(
    title="Pharma AI Backend",
    description="Multi-agent AI platform for pharmaceutical sales",
    version="1.0.0"
)

# CORS - ALLOW EVERYTHING (we'll restrict later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
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
        "message": "Pharma AI Backend - Multi-Agent System",
        "status": "operational",
        "version": "1.0.0",
        "agents": ["sales", "medical", "compliance", "hcp_persona", "audit"],
        "ai_enabled": True,
        "endpoints": {
            "health": "/health",
            "query": "/api/query",
            "agents": "/api/agents/status",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health_check():
    openai_configured = bool(os.getenv("OPENAI_API_KEY"))
    return {
        "status": "healthy",
        "version": "1.0.0",
        "openai_configured": openai_configured,
        "timestamp": time.time()
    }

@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        result = await orchestrator.process_query(
            query=request.query,
            user_id=request.user_id,
            hcp_context=request.hcp_context
        )
        
        return QueryResponse(
            query=request.query,
            response=result["response"],
            agents_used=result["agents_used"],
            compliance_status=ComplianceCheck(**result["compliance_status"]),
            response_time_seconds=result["response_time_seconds"]
        )
        
    except Exception as e:
        print(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/api/agents/status")
def get_agent_status():
    openai_configured = bool(os.getenv("OPENAI_API_KEY"))
    return {
        "total_agents": 5,
        "agents": [
            {"name": "sales_agent", "status": "active" if openai_configured else "offline", "version": "1.0.0"},
            {"name": "medical_agent", "status": "planned", "version": "1.0.0"},
            {"name": "compliance_guardian", "status": "active", "version": "1.0.0"},
            {"name": "hcp_persona_agent", "status": "planned", "version": "1.0.0"},
            {"name": "audit_agent", "status": "active", "version": "1.0.0"}
        ],
        "system_status": "operational" if openai_configured else "configuration_required",
        "openai_configured": openai_configured
    }

@app.on_event("startup")
async def startup_event():
    print("🚀 Pharma AI Backend starting up...")
    if os.getenv("OPENAI_API_KEY"):
        print("✅ OpenAI API key configured")
    else:
        print("⚠️  WARNING: OPENAI_API_KEY not set!")
    print("📊 Agents initialized")
    print("✅ Server ready!")

@app.on_event("shutdown")
async def shutdown_event():
    print("👋 Pharma AI Backend shutting down...")

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*50)
    print("🏥 PHARMA AI - MULTI-AGENT SYSTEM")
    print("="*50)
    print("\n�� Starting server on http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("❤️  Health Check: http://localhost:8000/health")
    print("\n⌨️  Press CTRL+C to stop\n")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, log_level="info")
