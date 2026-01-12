"""
Conversation Analysis Agent - Strict Scoring Version
"""

from typing import Dict, Optional
import json
import os
from openai import OpenAI

STRICT_SCORING_PROMPT = """You are a strict pharmaceutical sales conversation analyst. Your job is to identify problems and rate accurately - DO NOT be generous with scores.

STRICT SCORING GUIDELINES:

**COMPLIANCE (0-5):**
- 5.0: Perfect. Zero issues.
- 4.0: Minor vagueness but no violations
- 3.0: Borderline statements that need clarification
- 2.0: Clear policy violations (not off-label)
- 0-1.0: OFF-LABEL PROMOTION = AUTOMATIC ZERO

**TONE & PROFESSIONALISM (0-5):**
- 5.0: Highly professional, respectful, empathetic
- 4.0: Professional but could be warmer
- 3.0: Acceptable but impersonal or slightly pushy
- 2.0: Pushy, dismissive, or inappropriate language
- 0-1.0: Rude, aggressive, or unprofessional

**PRODUCT KNOWLEDGE (0-5):**
- 5.0: Cites specific studies, data, mechanisms
- 4.0: Good general knowledge, some specifics
- 3.0: Vague claims ("it's better", "everyone uses it")
- 2.0: Incorrect information or obvious gaps
- 0-1.0: False claims or major errors

**OBJECTION HANDLING (0-5):**
- 5.0: Acknowledges + data-driven response + addresses root concern
- 4.0: Addresses objection with some data
- 3.0: Generic response without real resolution
- 2.0: Ignores objection or becomes defensive
- 0-1.0: Dismisses doctor's concerns

**RELATIONSHIP BUILDING (0-5):**
- 5.0: Highly personalized, references doctor's situation, builds rapport
- 4.0: Some personalization, respectful
- 3.0: Transactional, minimal relationship effort
- 2.0: Generic, treats doctor as target not partner
- 0-1.0: Disrespectful or manipulative

**CALL-TO-ACTION (0-5):**
- 5.0: Specific date/time, clear action, mutual commitment
- 4.0: Clear next step with timeframe
- 3.0: Vague follow-up ("I'll send you stuff")
- 2.0: No clear next steps
- 0-1.0: Pushy or presumptive close

RED FLAGS (automatic score reductions):
- Off-label mentions → Compliance = 0.0
- "Everyone's using it" → Knowledge = max 2.0
- Pushy closing ("put you down for X patients") → Tone = max 2.0
- "You get what you pay for" (dismissive) → Objection Handling = max 2.0
- No specific follow-up date/time → CTA = max 3.0
- Interrupts doctor or ignores concerns → Tone = max 2.0

Conversation to analyze:
---
{conversation}
---

Rep: {rep_name}
Doctor: {doctor_name}

BE HARSH. Most conversations should score 3.0-3.8. Only truly excellent conversations deserve 4.5+.

Return ONLY this JSON:
{{
  "overall_score": 3.2,
  "overall_color": "yellow",
  "scores": {{
    "compliance": {{"score": 4.0, "color": "green", "justification": "Specific reason with quote", "examples": ["exact quote"], "dimension": "Compliance"}},
    "tone": {{"score": 3.0, "color": "yellow", "justification": "Specific reason", "examples": ["quote"], "dimension": "Tone & Professionalism"}},
    "knowledge": {{"score": 3.5, "color": "yellow", "justification": "Why score", "examples": ["quote"], "dimension": "Product Knowledge"}},
    "objection_handling": {{"score": 2.5, "color": "red", "justification": "What was wrong", "examples": ["quote"], "dimension": "Objection Handling"}},
    "relationship": {{"score": 3.0, "color": "yellow", "justification": "Explain", "examples": ["quote"], "dimension": "Relationship Building"}},
    "call_to_action": {{"score": 2.8, "color": "red", "justification": "Why low", "examples": ["quote"], "dimension": "Call-to-Action"}}
  }},
  "strengths": ["Specific strength with example"],
  "improvements": ["Specific actionable improvement"],
  "coaching": [
    {{"issue": "Specific problem found", "recommendation": "Exactly what to do instead", "example": "Exact words to say"}}
  ],
  "conversation_summary": "2-sentence summary"
}}"""

def analyze_conversation_sync(
    conversation: str,
    rep_name: Optional[str] = "Sales Rep",
    doctor_name: Optional[str] = "Dr. Smith"
) -> Dict:
    """Analyze with strict scoring."""
    
    try:
        print(f"[ANALYZER] Analyzing: {rep_name} with {doctor_name}")
        
        # Create client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found")
        
        client = OpenAI(api_key=api_key)
        
        # Format prompt
        prompt = STRICT_SCORING_PROMPT.format(
            conversation=conversation,
            rep_name=rep_name,
            doctor_name=doctor_name
        )
        
        print("[ANALYZER] Calling OpenAI with strict scoring...")
        
        # Call with LOWER temperature for consistency
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a strict sales analyst. Be critical. Most conversations have problems. Return only JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,  # VERY LOW for consistent, critical scoring
            max_tokens=2000
        )
        
        result_text = response.choices[0].message.content
        print(f"[ANALYZER] Got response ({len(result_text)} chars)")
        
        # Clean up
        result_text = result_text.strip()
        
        # Remove markdown
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0]
        elif "```" in result_text:
            parts = result_text.split("```")
            if len(parts) >= 2:
                result_text = parts[1]
        
        result_text = result_text.strip()
        
        # Extract JSON
        start = result_text.find('{')
        end = result_text.rfind('}')
        
        if start == -1 or end == -1:
            raise ValueError("No JSON found")
        
        json_text = result_text[start:end+1]
        
        # Parse
        analysis = json.loads(json_text)
        
        # Add metadata
        analysis["rep_name"] = rep_name
        analysis["doctor_name"] = doctor_name
        
        print(f"[ANALYZER] Score: {analysis.get('overall_score')}")
        
        return analysis
        
    except Exception as e:
        print(f"[ANALYZER] ERROR: {str(e)}")
        raise Exception(f"Analysis failed: {str(e)}")

# Async wrapper
async def analyze_conversation(
    conversation: str,
    rep_name: Optional[str] = "Sales Rep",
    doctor_name: Optional[str] = "Dr. Smith"
) -> Dict:
    """Async wrapper."""
    return analyze_conversation_sync(conversation, rep_name, doctor_name)
