"""
Conversation Analysis Agent - Few-Shot Learning Version
"""

from typing import Dict, Optional
import json
import os
from openai import OpenAI

FEW_SHOT_EXAMPLES = """
EXAMPLE 1 - EXCELLENT CONVERSATION (Score: 4.8):
Rep: "Our latest study published in JAMA Cardiology showed 42% lower side effects and 78% adherence at 12 months."
Dr: "What about cost?"
Rep: "When we look at total cost of care, patients had 31% fewer cardiovascular events. One prevented hospitalization averaging $48,000 offsets three years of medication cost. We also have patient assistance covering 80% of costs."
Dr: "Send me the study."
Rep: "I'll email the JAMA study today. Can we schedule 20 minutes next Thursday at 2pm to discuss?"

WHY 4.8:
- Compliance: 5.0 (cites specific published study, no violations)
- Tone: 5.0 (professional, respectful)
- Knowledge: 5.0 (specific data: "42%", "78%", "JAMA Cardiology", "31%", "$48,000")
- Objection: 5.0 (acknowledges cost, pivots to total cost with hard data)
- Relationship: 4.5 (respectful, offers assistance program)
- CTA: 5.0 (specific date/time: "Thursday at 2pm")

EXAMPLE 2 - POOR WITH COMPLIANCE VIOLATION (Score: 1.2):
Rep: "Officially it's for hyperlipidemia, but between you and me, we're seeing amazing results for migraines too."
Dr: "That's not an approved indication."
Rep: "Everyone does off-label. Your competitor is prescribing it for migraines."

WHY 1.2:
- Compliance: 0.0 (CRITICAL: Off-label promotion for migraines = automatic zero)
- Tone: 2.0 (unprofessional: "between you and me", pressures with competitor)
- Knowledge: 1.5 (vague: "amazing results", no data)
- Objection: 1.0 (dismissive: "everyone does it")
- Relationship: 1.5 (manipulative: competitor pressure)
- CTA: 2.0 (no clear next step)

EXAMPLE 3 - MEDIOCRE/PUSHY (Score: 2.8):
Rep: "CardioStatin is the best on the market. Everyone's switching."
Dr: "I'm using generics."
Rep: "Yeah but CardioStatin is way better."
Dr: "Do you have data?"
Rep: "We have tons of studies. You should just try it. It costs more but you get what you pay for."

WHY 2.8:
- Compliance: 4.0 (no violations, but vague claims)
- Tone: 2.5 (pushy: "you should just try it", dismissive of cost)
- Knowledge: 2.0 (vague: "the best", "way better", no specifics)
- Objection: 2.0 (dismissive: "you get what you pay for")
- Relationship: 2.5 (transactional, no rapport building)
- CTA: 3.0 (vague: "I'll send stuff", no specific date)
"""

SCORING_PROMPT = """You are a pharmaceutical sales analyst. Use the examples above to calibrate your scoring.

CRITICAL RULES:
1. OFF-LABEL PROMOTION = Compliance score MUST be 0.0, overall score MUST be below 2.0
2. Specific data (studies, percentages, dollar amounts) = 4.5-5.0 for Knowledge
3. Vague claims ("better", "everyone uses") = max 3.0 for Knowledge
4. Specific date/time in CTA = 4.5-5.0, vague follow-up = max 3.0
5. Data-driven objection handling = 4.5-5.0, dismissive = max 2.5

NOW ANALYZE THIS CONVERSATION:
---
{conversation}
---

Look for:
- OFF-LABEL mentions (migraines, pain, inflammation for a cholesterol drug) → Compliance = 0.0
- Specific studies, journals, percentages → Knowledge = high
- Pushy language ("put you down for", "you should", "just try") → Tone = low
- Specific date/time → CTA = high
- Vague ("I'll send stuff") → CTA = low

Return ONLY JSON:
{{
  "overall_score": 2.8,
  "overall_color": "yellow",
  "scores": {{
    "compliance": {{"score": 0.0, "color": "red", "justification": "Off-label promotion detected", "examples": ["quote"], "dimension": "Compliance"}},
    "tone": {{"score": 2.5, "color": "red", "justification": "Pushy language", "examples": ["quote"], "dimension": "Tone & Professionalism"}},
    "knowledge": {{"score": 2.0, "color": "red", "justification": "Vague claims, no data", "examples": ["quote"], "dimension": "Product Knowledge"}},
    "objection_handling": {{"score": 2.0, "color": "red", "justification": "Dismissive", "examples": ["quote"], "dimension": "Objection Handling"}},
    "relationship": {{"score": 2.5, "color": "red", "justification": "Transactional", "examples": ["quote"], "dimension": "Relationship Building"}},
    "call_to_action": {{"score": 3.0, "color": "yellow", "justification": "Vague follow-up", "examples": ["quote"], "dimension": "Call-to-Action"}}
  }},
  "strengths": ["One specific strength if any"],
  "improvements": ["Specific actionable fix"],
  "coaching": [{{"issue": "Problem", "recommendation": "Solution", "example": "What to say"}}],
  "conversation_summary": "Brief summary"
}}

Rep: {rep_name}, Doctor: {doctor_name}, Product: CardioStatin (cholesterol med)
"""

def analyze_conversation_sync(
    conversation: str,
    rep_name: Optional[str] = "Sales Rep",
    doctor_name: Optional[str] = "Dr. Smith"
) -> Dict:
    """Analyze with few-shot learning."""
    
    try:
        print(f"[ANALYZER] Analyzing: {rep_name} with {doctor_name}")
        
        # Check for off-label keywords first
        off_label_keywords = [
            "migraine", "headache", "pain", "inflammation", 
            "off-label", "other uses", "also works for",
            "between you and me", "unofficially"
        ]
        
        conversation_lower = conversation.lower()
        has_off_label = any(keyword in conversation_lower for keyword in off_label_keywords)
        
        if has_off_label:
            print("[ANALYZER] ⚠️  OFF-LABEL KEYWORDS DETECTED!")
        
        # Create client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found")
        
        client = OpenAI(api_key=api_key)
        
        # Combine examples + prompt
        full_prompt = FEW_SHOT_EXAMPLES + "\n\n" + SCORING_PROMPT.format(
            conversation=conversation,
            rep_name=rep_name,
            doctor_name=doctor_name
        )
        
        print("[ANALYZER] Calling OpenAI with few-shot examples...")
        
        # Use GPT-4 for better reasoning (or gpt-4o-mini with very low temp)
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Could upgrade to "gpt-4o" for better accuracy
            messages=[
                {
                    "role": "system", 
                    "content": "You are a strict pharmaceutical sales analyst. Follow the examples precisely. Off-label promotion MUST score 0.0 for compliance. Be harsh - most conversations are mediocre (2.5-3.5). Only truly excellent ones score 4.5+."
                },
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.05,  # VERY low for consistency
            max_tokens=2000
        )
        
        result_text = response.choices[0].message.content
        print(f"[ANALYZER] Response length: {len(result_text)}")
        
        # Clean up
        result_text = result_text.strip()
        
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
        analysis = json.loads(json_text)
        
        # ENFORCE compliance rule if off-label detected
        if has_off_label:
            print("[ANALYZER] ENFORCING: Compliance = 0.0 (off-label detected)")
            if "scores" in analysis and "compliance" in analysis["scores"]:
                analysis["scores"]["compliance"]["score"] = 0.0
                analysis["scores"]["compliance"]["color"] = "red"
                if "off-label" not in analysis["scores"]["compliance"]["justification"].lower():
                    analysis["scores"]["compliance"]["justification"] = "CRITICAL VIOLATION: Off-label promotion detected"
            
            # Recalculate overall score
            if "scores" in analysis:
                scores_list = [s["score"] for s in analysis["scores"].values()]
                analysis["overall_score"] = round(sum(scores_list) / len(scores_list), 1)
                analysis["overall_color"] = "red" if analysis["overall_score"] < 3.0 else "yellow"
        
        # Add metadata
        analysis["rep_name"] = rep_name
        analysis["doctor_name"] = doctor_name
        
        print(f"[ANALYZER] Final score: {analysis.get('overall_score')}")
        
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
