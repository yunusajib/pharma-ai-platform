"""
Conversation Analysis Agent - Debug Version
"""

from typing import Dict, Optional
import json
import os

def analyze_conversation_sync(
    conversation: str,
    rep_name: Optional[str] = "Sales Rep",
    doctor_name: Optional[str] = "Dr. Smith"
) -> Dict:
    """Analyze conversation with extensive debugging."""
    
    print("="*60)
    print("[ANALYZER] === STARTING ANALYSIS ===")
    print(f"[ANALYZER] Rep: {rep_name}, Doctor: {doctor_name}")
    print(f"[ANALYZER] Conversation length: {len(conversation)} chars")
    print("="*60)
    
    try:
        # Import OpenAI
        print("[ANALYZER] Step 1: Importing OpenAI...")
        from openai import OpenAI
        print("[ANALYZER] Step 1: ✓ OpenAI imported")
        
        # Get API key
        print("[ANALYZER] Step 2: Getting API key...")
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found")
        print(f"[ANALYZER] Step 2: ✓ API key found (length: {len(api_key)})")
        
        # Create client
        print("[ANALYZER] Step 3: Creating OpenAI client...")
        client = OpenAI(api_key=api_key)
        print("[ANALYZER] Step 3: ✓ Client created")
        
        # Create prompt
        print("[ANALYZER] Step 4: Creating prompt...")
        prompt = f"""Analyze this conversation and return ONLY valid JSON:

Conversation:
{conversation}

Return exactly this format:
{{
  "overall_score": 4.0,
  "overall_color": "green",
  "scores": {{
    "compliance": {{"score": 5.0, "color": "green", "justification": "Good", "examples": ["quote"], "dimension": "Compliance"}},
    "tone": {{"score": 4.0, "color": "green", "justification": "Good", "examples": ["quote"], "dimension": "Tone & Professionalism"}},
    "knowledge": {{"score": 4.0, "color": "green", "justification": "Good", "examples": ["quote"], "dimension": "Product Knowledge"}},
    "objection_handling": {{"score": 3.5, "color": "yellow", "justification": "Ok", "examples": ["quote"], "dimension": "Objection Handling"}},
    "relationship": {{"score": 4.0, "color": "green", "justification": "Good", "examples": ["quote"], "dimension": "Relationship Building"}},
    "call_to_action": {{"score": 3.5, "color": "yellow", "justification": "Ok", "examples": ["quote"], "dimension": "Call-to-Action"}}
  }},
  "strengths": ["Good compliance", "Professional tone"],
  "improvements": ["Better CTA"],
  "coaching": [{{"issue": "CTA vague", "recommendation": "Be specific", "example": "Let's meet Tuesday at 2pm"}}],
  "conversation_summary": "Brief summary"
}}"""
        print(f"[ANALYZER] Step 4: ✓ Prompt created ({len(prompt)} chars)")
        
        # Call OpenAI
        print("[ANALYZER] Step 5: Calling OpenAI API...")
        print("[ANALYZER] Step 5: Model: gpt-4o-mini, temp: 0.3, max_tokens: 2000")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        
        print("[ANALYZER] Step 5: ✓ Got response from OpenAI")
        
        # Extract content
        print("[ANALYZER] Step 6: Extracting content...")
        result_text = response.choices[0].message.content
        print(f"[ANALYZER] Step 6: ✓ Content extracted (length: {len(result_text)})")
        print("[ANALYZER] Step 6: First 500 characters:")
        print("-" * 60)
        print(result_text[:500])
        print("-" * 60)
        
        # Clean up
        print("[ANALYZER] Step 7: Cleaning up response...")
        original_length = len(result_text)
        result_text = result_text.strip()
        
        # Remove markdown
        if "```json" in result_text:
            print("[ANALYZER] Step 7: Removing ```json markdown")
            result_text = result_text.split("```json")[1].split("```")[0]
        elif "```" in result_text:
            print("[ANALYZER] Step 7: Removing ``` markdown")
            parts = result_text.split("```")
            if len(parts) >= 2:
                result_text = parts[1]
        
        result_text = result_text.strip()
        print(f"[ANALYZER] Step 7: ✓ Cleaned (was {original_length}, now {len(result_text)})")
        
        # Find JSON
        print("[ANALYZER] Step 8: Finding JSON boundaries...")
        start = result_text.find('{')
        end = result_text.rfind('}')
        
        print(f"[ANALYZER] Step 8: First '{{' at position {start}")
        print(f"[ANALYZER] Step 8: Last '}}' at position {end}")
        
        if start == -1 or end == -1:
            print("[ANALYZER] Step 8: ✗ No JSON found!")
            print("[ANALYZER] Full text:")
            print(result_text)
            raise ValueError("No JSON object found")
        
        json_text = result_text[start:end+1]
        print(f"[ANALYZER] Step 8: ✓ Extracted JSON ({len(json_text)} chars)")
        print("[ANALYZER] Step 8: First 500 chars of JSON:")
        print("-" * 60)
        print(json_text[:500])
        print("-" * 60)
        
        # Parse JSON
        print("[ANALYZER] Step 9: Parsing JSON...")
        analysis = json.loads(json_text)
        print("[ANALYZER] Step 9: ✓ JSON parsed successfully!")
        print(f"[ANALYZER] Step 9: Overall score: {analysis.get('overall_score')}")
        
        # Add metadata
        print("[ANALYZER] Step 10: Adding metadata...")
        analysis["rep_name"] = rep_name
        analysis["doctor_name"] = doctor_name
        print("[ANALYZER] Step 10: ✓ Metadata added")
        
        print("="*60)
        print("[ANALYZER] === ANALYSIS COMPLETE ===")
        print("="*60)
        
        return analysis
        
    except Exception as e:
        print("="*60)
        print(f"[ANALYZER] === ERROR OCCURRED ===")
        print(f"[ANALYZER] Error type: {type(e).__name__}")
        print(f"[ANALYZER] Error message: {str(e)}")
        print(f"[ANALYZER] Error repr: {repr(e)}")
        print("="*60)
        import traceback
        print("[ANALYZER] Full traceback:")
        traceback.print_exc()
        print("="*60)
        raise Exception(f"Analysis failed: {str(e)}")

# Async wrapper
async def analyze_conversation(
    conversation: str,
    rep_name: Optional[str] = "Sales Rep",
    doctor_name: Optional[str] = "Dr. Smith"
) -> Dict:
    """Async wrapper."""
    return analyze_conversation_sync(conversation, rep_name, doctor_name)
