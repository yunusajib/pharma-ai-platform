"""
Conversation Analysis Agent
Analyzes sales rep conversations with healthcare professionals
Provides scores, feedback, and coaching recommendations
"""

from typing import Dict, List, Optional
import json
from .openai_client import get_openai_client

CONVERSATION_ANALYZER_PROMPT = """You are an expert pharmaceutical sales conversation analyst with 20+ years of experience coaching medical sales representatives.

Analyze the following conversation between a sales representative and a healthcare professional (HCP).

Score the conversation on these 6 critical dimensions (scale 0-5):

1. **Compliance** (0-5): Regulatory adherence, no off-label promotion, accurate claims
   - 5: Perfect compliance, all statements backed by approved indications
   - 3: Minor compliance concerns, vague statements
   - 1: Clear violations, off-label promotion detected

2. **Tone & Professionalism** (0-5): Respectful language, appropriate formality, empathy
   - 5: Highly professional, empathetic, builds trust
   - 3: Professional but impersonal or occasionally pushy
   - 1: Rude, dismissive, or overly aggressive

3. **Product Knowledge** (0-5): Accuracy, depth, confidence in explanations
   - 5: Expert-level knowledge, handles complex questions confidently
   - 3: Basic knowledge, some hesitation or vagueness
   - 1: Factual errors, inability to answer questions

4. **Objection Handling** (0-5): Addresses concerns effectively, pivots to value
   - 5: Acknowledges concerns, provides data-driven responses, turns objections into opportunities
   - 3: Addresses some concerns but misses key points
   - 1: Ignores objections, becomes defensive, or gives inadequate responses

5. **Relationship Building** (0-5): Personalization, rapport, understanding HCP needs
   - 5: Highly personalized, references HCP's specific situation, builds strong rapport
   - 3: Some personalization, generic relationship-building attempts
   - 1: Completely transactional, no personalization

6. **Call-to-Action** (0-5): Clear next steps, specific follow-up, commitment
   - 5: Specific action with date/time, mutual commitment established
   - 3: Vague next steps, no specific timeline
   - 1: No clear follow-up, ends abruptly

For each dimension provide:
- Numeric score (0-5, use decimals like 4.5)
- Brief justification (2-3 sentences)
- Specific examples from the conversation (quote exact phrases)
- Color code: "red" (<3.0), "yellow" (3.0-3.9), "green" (≥4.0)

Also provide:
- Overall score (average of all 6 dimensions)
- Top 3 strengths (what the rep did well)
- Top 3 areas for improvement (specific, actionable)
- 3-5 coaching recommendations with:
  * The issue/gap identified
  * Specific recommendation
  * Example of what they should have said

**IMPORTANT**: Return ONLY valid JSON, no markdown formatting, no additional text.

Return this exact JSON structure:
{
  "overall_score": 4.2,
  "overall_color": "green",
  "scores": {
    "compliance": {
      "score": 5.0,
      "color": "green",
      "justification": "...",
      "examples": ["Specific quote from conversation", "Another quote"],
      "dimension": "Compliance"
    },
    "tone": {
      "score": 4.5,
      "color": "green",
      "justification": "...",
      "examples": ["Quote showing good tone"],
      "dimension": "Tone & Professionalism"
    },
    "knowledge": {
      "score": 4.0,
      "color": "green",
      "justification": "...",
      "examples": ["Quote showing product knowledge"],
      "dimension": "Product Knowledge"
    },
    "objection_handling": {
      "score": 3.5,
      "color": "yellow",
      "justification": "...",
      "examples": ["Quote showing objection handling"],
      "dimension": "Objection Handling"
    },
    "relationship": {
      "score": 4.5,
      "color": "green",
      "justification": "...",
      "examples": ["Quote showing relationship building"],
      "dimension": "Relationship Building"
    },
    "call_to_action": {
      "score": 3.8,
      "color": "yellow",
      "justification": "...",
      "examples": ["Quote showing CTA"],
      "dimension": "Call-to-Action"
    }
  },
  "strengths": [
    "Perfect regulatory compliance throughout the conversation",
    "Strong rapport building with personalized approach",
    "Confident product knowledge demonstrated"
  ],
  "improvements": [
    "Objection handling: Could have provided ROI data when cost was mentioned",
    "Call-to-action was vague - needed specific date/time for follow-up",
    "Used doctor's name only once - should use it more frequently"
  ],
  "coaching": [
    {
      "issue": "When Dr mentioned cost concerns, rep didn't pivot to value proposition effectively",
      "recommendation": "Acknowledge cost concern, then immediately pivot to outcomes data and total cost of care",
      "example": "I understand cost is important. Many practices actually find that CardioStatin reduces overall costs because patients have 30% fewer cardiac events, which means fewer ER visits and hospitalizations."
    }
  ],
  "conversation_summary": "Brief 2-3 sentence summary of the conversation flow and outcome"
}

**Conversation to analyze:**

{conversation}

**Additional Context:**
- Rep Name: {rep_name}
- Doctor Name: {doctor_name}
- Product: CardioStatin (cholesterol medication)

Return ONLY the JSON object above, no other text.
"""

async def analyze_conversation(
    conversation: str,
    rep_name: Optional[str] = "Sales Rep",
    doctor_name: Optional[str] = "Healthcare Professional"
) -> Dict:
    """
    Analyze a sales conversation and return detailed scores and coaching.
    
    Args:
        conversation: The conversation transcript
        rep_name: Name of the sales representative
        doctor_name: Name of the healthcare professional
        
    Returns:
        Dict with scores, feedback, and coaching recommendations
    """
    try:
        client = get_openai_client()
        
        # Format the prompt
        prompt = CONVERSATION_ANALYZER_PROMPT.format(
            conversation=conversation,
            rep_name=rep_name,
            doctor_name=doctor_name
        )
        
        # Call OpenAI
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert pharmaceutical sales conversation analyst. Always return valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,  # Lower temperature for more consistent scoring
            max_tokens=2000
        )
        
        # Extract and parse the response
        result_text = response.choices[0].message.content.strip()
        
        # Remove markdown code fences if present
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.startswith("```"):
            result_text = result_text[3:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]
        
        result_text = result_text.strip()
        
        # Parse JSON
        analysis = json.loads(result_text)
        
        # Add metadata
        analysis["rep_name"] = rep_name
        analysis["doctor_name"] = doctor_name
        analysis["analyzed_at"] = "timestamp_placeholder"
        
        return analysis
        
    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {e}")
        print(f"Response text: {result_text}")
        raise Exception(f"Failed to parse AI response as JSON: {str(e)}")
    except Exception as e:
        print(f"Analysis error: {str(e)}")
        raise Exception(f"Failed to analyze conversation: {str(e)}")


def get_score_color(score: float) -> str:
    """Determine color based on score"""
    if score >= 4.0:
        return "green"
    elif score >= 3.0:
        return "yellow"
    else:
        return "red"


def get_performance_level(score: float) -> str:
    """Get performance level text"""
    if score >= 4.5:
        return "Excellent"
    elif score >= 4.0:
        return "Good"
    elif score >= 3.0:
        return "Needs Improvement"
    else:
        return "Critical Issues"
