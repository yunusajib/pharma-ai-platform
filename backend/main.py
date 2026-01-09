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
    description="Multi-agent AI platform for pharmaceutical sales",
    version="1.0.0"
)

orchestrator = AgentOrchestrator()

# CORS headers for all responses
def cors_response(content, status_code=200):
    return JSONResponse(
        content=content,
        status_code=status_code,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Max-Age": "3600",
        }
    )

# Handle OPTIONS for all routes
@app.options("/{full_path:path}")
async def options_handler():
    return cors_response({"status": "ok"})

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
    return cors_response({
        "message": "Pharma AI Backend - Multi-Agent System",
        "status": "operational",
        "version": "1.0.0",
        "agents": ["sales", "medical", "compliance", "hcp_persona", "audit"],
        "ai_enabled": True,
    })

@app.get("/health")
def health_check():
    openai_configured = bool(os.getenv("OPENAI_API_KEY"))
    return cors_response({
        "status": "healthy",
        "version": "1.0.0",
        "openai_configured": openai_configured,
        "timestamp": time.time()
    })

@app.post("/api/query")
async def process_query(request: QueryRequest):
    try:
        result = await orchestrator.process_query(
            query=request.query,
            user_id=request.user_id,
            hcp_context=request.hcp_context
        )
        
        response_data = {
            "query": request.query,
            "response": result["response"],
            "agents_used": result["agents_used"],
            "compliance_status": result["compliance_status"],
            "response_time_seconds": result["response_time_seconds"]
        }
        
        return cors_response(response_data)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return cors_response({"detail": str(e)}, status_code=500)

@app.get("/api/agents/status")
def get_agent_status():
    openai_configured = bool(os.getenv("OPENAI_API_KEY"))
    return cors_response({
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
    })

@app.on_event("startup")
async def startup_event():
    print("🚀 Pharma AI Backend starting up...")
    if os.getenv("OPENAI_API_KEY"):
        print("✅ OpenAI API key configured")
    else:
        print("⚠️ WARNING: OPENAI_API_KEY not set!")
    print("📊 Agents initialized")
    print("✅ Server ready!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
