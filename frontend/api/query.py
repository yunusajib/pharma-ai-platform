from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from mangum import Mangum
import os
import time

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    user_id: str
    hcp_context: Optional[dict] = None

@app.post("/api/query")
async def process_query(request: QueryRequest):
    # Simple mock response for now
    # TODO: Add your agent logic here
    
    query_lower = request.query.lower()
    
    # Check for off-label
    if any(word in query_lower for word in ["migraine", "off-label", "headache prevention"]):
        return JSONResponse({
            "query": request.query,
            "response": "⚠️ COMPLIANCE ALERT: This request was blocked to protect you from regulatory risk. This question implies off-label use. Our drug is not FDA-approved for this indication.",
            "agents_used": ["compliance_guardian"],
            "compliance_status": {
                "status": "BLOCKED",
                "violation_type": "off_label_promotion",
                "explanation": "Question about unapproved indication detected."
            },
            "response_time_seconds": 0.1
        })
    
    # Approved response
    return JSONResponse({
        "query": request.query,
        "response": f"Based on your question about '{request.query}', here's strategic sales advice:\n\n1. Lead with value proposition\n2. Address objections with data\n3. Focus on patient outcomes\n\nFor detailed clinical information, please consult Medical Affairs.",
        "agents_used": ["sales_agent", "compliance_guardian"],
        "compliance_status": {
            "status": "APPROVED",
            "violation_type": None,
            "explanation": None
        },
        "response_time_seconds": 0.5
    })

# Mangum handler for Vercel
handler = Mangum(app)
