from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv
import time

# Import our agent system
from agents.orchestrator import AgentOrchestrator

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Pharma AI Backend",
    description="Multi-agent AI platform for pharmaceutical sales",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent orchestrator
orchestrator = AgentOrchestrator()

# ============================================
# REQUEST/RESPONSE MODELS
# ============================================


class QueryRequest(BaseModel):
    """User query request"""
    query: str
    user_id: str
    hcp_context: Optional[dict] = None


class ComplianceCheck(BaseModel):
    """Compliance status response"""
    status: str
    violation_type: Optional[str] = None
    explanation: Optional[str] = None


class QueryResponse(BaseModel):
    """Complete query response with compliance info"""
    query: str
    response: str
    agents_used: List[str]
    compliance_status: ComplianceCheck
    response_time_seconds: float

# ============================================
# API ENDPOINTS
# ============================================


@app.get("/")
def read_root():
    """Root endpoint - API info"""
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
    """Health check endpoint"""
    # Check if OpenAI key is configured
    openai_configured = bool(os.getenv("OPENAI_API_KEY"))

    return {
        "status": "healthy",
        "version": "1.0.0",
        "openai_configured": openai_configured,
        "timestamp": time.time()
    }


@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Main query endpoint - processes user questions through AI agents.
    Now with REAL AI integration!
    """
    try:
        # Process through agent orchestrator
        result = await orchestrator.process_query(
            query=request.query,
            user_id=request.user_id,
            hcp_context=request.hcp_context
        )

        # Format response
        return QueryResponse(
            query=request.query,
            response=result["response"],
            agents_used=result["agents_used"],
            compliance_status=ComplianceCheck(**result["compliance_status"]),
            response_time_seconds=result["response_time_seconds"]
        )

    except Exception as e:
        # Log error (in production, use proper logging)
        print(f"Error processing query: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


@app.get("/api/agents/status")
def get_agent_status():
    """Returns status of all AI agents"""
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

# ============================================
# STARTUP/SHUTDOWN EVENTS
# ============================================


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print("🚀 Pharma AI Backend starting up...")

    # Check OpenAI configuration
    if os.getenv("OPENAI_API_KEY"):
        print("✅ OpenAI API key configured")
    else:
        print("⚠️  WARNING: OPENAI_API_KEY not set! Add it to .env file")

    print("📊 Agents initialized")
    print("✅ Server ready!")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    print("👋 Pharma AI Backend shutting down...")

# ============================================
# RUN SERVER
# ============================================

if __name__ == "__main__":
    import uvicorn

    print("\n" + "="*50)
    print("🏥 PHARMA AI - MULTI-AGENT SYSTEM")
    print("="*50)
    print("\n📍 Starting server on http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("❤️  Health Check: http://localhost:8000/health")
    print("\n⌨️  Press CTRL+C to stop\n")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
