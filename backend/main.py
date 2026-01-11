from fastapi import FastAPI, HTTPException
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
        "message": "Pharma AI Backend - Multi-Agent System",
        "status": "operational",
        "version": "1.0.0",
        "endpoints": ["/health", "/api/query", "/api/agents/status", "/docs"]
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
        print(f"[API] Received query: {request.query}")

        result = await orchestrator.process_query(
            query=request.query,
            user_id=request.user_id,
            hcp_context=request.hcp_context
        )

        print(f"[API] Query processed successfully")

        return QueryResponse(
            query=request.query,
            response=result["response"],
            agents_used=result["agents_used"],
            compliance_status=ComplianceCheck(**result["compliance_status"]),
            response_time_seconds=result["response_time_seconds"]
        )

    except Exception as e:
        print(f"[API] Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/agents/status")
def get_agent_status():
    openai_configured = bool(os.getenv("OPENAI_API_KEY"))
    return {
        "total_agents": 5,
        "agents": [
            {"name": "sales_agent",
                "status": "active" if openai_configured else "offline", "version": "1.0.0"},
            {"name": "medical_agent", "status": "planned", "version": "1.0.0"},
            {"name": "compliance_guardian", "status": "active", "version": "1.0.0"},
            {"name": "hcp_persona_agent", "status": "planned", "version": "1.0.0"},
            {"name": "audit_agent", "status": "active", "version": "1.0.0"}
        ],
        "system_status": "operational" if openai_configured else "configuration_required",
        "openai_configured": openai_configured
    }
# backend/main.py


class ConversationAnalysisRequest(BaseModel):
    conversation: str
    rep_name: Optional[str] = None
    doctor_name: Optional[str] = None


@app.post("/api/analyze-conversation")
async def analyze_sales_conversation(request: ConversationAnalysisRequest):
    try:
        result = await analyze_conversation(request.conversation)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("startup")
async def startup_event():
    print("="*50)
    print("🚀 Pharma AI Backend Starting")
    print("="*50)
    if os.getenv("OPENAI_API_KEY"):
        print("✅ OpenAI API key configured")
    else:
        print("⚠️  WARNING: OPENAI_API_KEY not set!")
    print("📊 Agents initialized")
    print("✅ Server ready!")
    print("="*50)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

# Conversation Analysis Endpoint
from agents.conversation_analyzer import analyze_conversation

class ConversationAnalysisRequest(BaseModel):
    conversation: str
    rep_name: Optional[str] = "Sales Rep"
    doctor_name: Optional[str] = "Dr. Smith"

class ConversationAnalysisResponse(BaseModel):
    overall_score: float
    overall_color: str
    scores: dict
    strengths: List[str]
    improvements: List[str]
    coaching: List[dict]
    conversation_summary: str
    rep_name: str
    doctor_name: str

@app.post("/api/analyze-conversation", response_model=ConversationAnalysisResponse)
async def analyze_sales_conversation(request: ConversationAnalysisRequest):
    """
    Analyze a sales conversation and provide detailed scoring and coaching.
    """
    try:
        print(f"[API] Analyzing conversation for {request.rep_name} with {request.doctor_name}")
        
        result = await analyze_conversation(
            conversation=request.conversation,
            rep_name=request.rep_name,
            doctor_name=request.doctor_name
        )
        
        print(f"[API] Analysis complete. Overall score: {result.get('overall_score')}")
        
        return result
        
    except Exception as e:
        print(f"[API] Error analyzing conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
