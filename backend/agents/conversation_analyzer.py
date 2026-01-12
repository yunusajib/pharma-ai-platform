"""
Conversation Analysis Agent
"""

from typing import Dict, Optional
import json
import re
from .openai_client import OpenAIClient

CONVERSATION_ANALYZER_PROMPT = """You are an expert pharmaceutical sales conversation analyst.

Analyze this conversation and return ONLY a JSON object (no markdown, no extra text):

{
  "overall_score": 4.2,
  "overall_color": "green",
  "scores": {
    "compliance": {"score": 5.0, "color": "green", "justification": "Perfect compliance", "examples": ["Quote"], "dimension": "Compliance"},
    "tone": {"score": 4.5, "color": "green", "justification": "Professional tone", "examples": ["Quote"], "dimension": "Tone & Professionalism"},
    "knowledge": {"score": 4.0, "color": "green", "justification": "Good knowledge", "examples": ["Quote"], "dimension": "Product Knowledge"},
    "objection_handling": {"score": 3.5, "color": "yellow", "justification": "Addressed concerns", "examples": ["Quote"], "dimension": "Objection Handling"},
    "relationship": {"score": 4.5, "color": "green", "justification": "Good rapport", "examples": ["Quote"], "dimension": "Relationship Building"},
    "call_to_action": {"score": 3.8, "color": "yellow", "justification": "CTA present", "examples": ["Quote"], "dimension": "Call-to-Action"}
  },
  "strengths": ["Strength 1", "Strength 2", "Strength 3"],
  "improvements": ["Improvement 1", "Improvement 2", "Improvement 3"],
  "coaching": [
    {"issue": "Issue description", "recommendation": "What to do", "example": "Example response"}
  ],
  "conversation_summary": "Brief summary"
}

Score each dimension 0-5. Use color: "green" (>=4.0), "yellow" (3.0-3.9), "red" (<3.0).

Conversation:
{conversation}

Rep: {rep_name}
Doctor: {doctor_name}
Product: CardioStatin

Return ONLY the JSON object.
"""

async def analyze_conversation(
    conversation: str,
    rep_name: Optional[str] = "Sales Rep",
    doctor_name: Optional[str] = "Dr. Smith"
) -> Dict:
    """Analyze conversation and return scores."""
    
    try:
        print(f"[ANALYZER] Starting analysis for {rep_name} with {doctor_name}")
        
        # Create client
        openai_client = OpenAIClient()
        
        # Format prompt
        prompt = CONVERSATION_ANALYZER_PROMPT.format(
            conversation=conversation,
            rep_name=rep_name,
            doctor_name=doctor_name
        )
        
        print("[ANALYZER] Calling OpenAI...")
        
        # Call OpenAI
        response_text = await openai_client.generate_response(
            system_prompt="You are a pharmaceutical sales analyst. Return ONLY valid JSON, no markdown.",
            user_message=prompt,
            temperature=0.3,
            max_tokens=2000
        )
        
        print(f"[ANALYZER] Received response (length: {len(response_text)})")
        print(f"[ANALYZER] First 200 chars: {response_text[:200]}")
        
        # Aggressive cleanup
        result_text = response_text.strip()
        
        # Remove markdown code blocks
        result_text = re.sub(r'^```json\s*', '', result_text)
        result_text = re.sub(r'^```\s*', '', result_text)
        result_text = re.sub(r'\s*```$', '', result_text)
        
        # Remove any leading/trailing whitespace again
        result_text = result_text.strip()
        
        print(f"[ANALYZER] Cleaned text (first 200 chars): {result_text[:200]}")
        
        # Try to find JSON object boundaries
        # Look for the first { and last }
        start_idx = result_text.find('{')
        end_idx = result_text.rfind('}')
        
        if start_idx == -1 or end_idx == -1:
            raise ValueError(f"No valid JSON object found in response: {result_text[:500]}")
        
        result_text = result_text[start_idx:end_idx+1]
        
        print(f"[ANALYZER] Extracted JSON (first 200 chars): {result_text[:200]}")
        
        # Parse JSON
        analysis = json.loads(result_text)
        
        print(f"[ANALYZER] Successfully parsed JSON. Overall score: {analysis.get('overall_score')}")
        
        # Add metadata
        analysis["rep_name"] = rep_name
        analysis["doctor_name"] = doctor_name
        
        return analysis
        
    except json.JSONDecodeError as e:
        error_msg = f"JSON parsing failed at position {e.pos}: {e.msg}"
        print(f"[ANALYZER] ERROR: {error_msg}")
        print(f"[ANALYZER] Problematic text: {result_text[max(0, e.pos-50):e.pos+50]}")
        raise Exception(error_msg)
        
    except Exception as e:
        print(f"[ANALYZER] ERROR: {str(e)}")
        raise Exception(f"Analysis failed: {str(e)}")
