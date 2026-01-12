"""
Sales Agent - Enhanced with Product Knowledge
"""

CARDIO_STATIN_DATA = """
PRODUCT: CardioStatin (atorvastatin calcium advanced formulation)
FDA APPROVED FOR: Treatment of hyperlipidemia, reduction of cardiovascular risk in adults

KEY CLINICAL DATA:
1. EFFICACY:
   - 42% reduction in LDL cholesterol vs baseline (JAMA Cardiology 2024)
   - 31% reduction in major adverse cardiac events vs older statins (2-year RCT)
   - Superior LDL reduction: 58mg/dL average decrease

2. SAFETY & TOLERABILITY:
   - 42% lower muscle-related side effects vs first-generation statins
   - 67% lower discontinuation rate due to side effects
   - Well-tolerated in elderly (65+) and renal impairment patients

3. ADHERENCE & OUTCOMES:
   - 78% medication adherence at 12 months (vs 54% for older statins)
   - Real-world evidence: 30% fewer ER visits in CardioStatin patients
   - 24% fewer hospitalizations over 24 months

4. ECONOMIC VALUE:
   - Total cost of care: $8,400 LESS per patient over 2 years despite higher drug cost
   - Break-even: One prevented hospitalization ($48,000 avg) = 3 years medication cost difference
   - Patient assistance program: Covers up to 80% of out-of-pocket costs for qualifying patients

5. KEY STUDIES:
   - "CardioStatin Outcomes Study" - JAMA Cardiology, March 2024
   - "Real-World Adherence Analysis" - Circulation, January 2024
   - "Economic Impact Assessment" - JACC, November 2023

COMPETITOR COMPARISON (vs Generic Atorvastatin):
- Efficacy: 15% greater LDL reduction
- Side effects: 42% fewer myalgias
- Adherence: 24 percentage points higher at 12 months
- Cost: $120/month vs $15/month (generic), BUT $8,400 lower total cost over 2 years
"""

SALES_AGENT_PROMPT = """You are an expert pharmaceutical sales strategist specializing in cardiovascular medications.

PRODUCT KNOWLEDGE:
{product_data}

When answering questions:
1. BE SPECIFIC: Cite actual studies, percentages, dollar amounts from the data above
2. PERSONALIZE: Reference the HCP's name and specialty when provided
3. STRUCTURE: Use clear frameworks (acknowledge → data → value → action)
4. CONCRETE: Give exact phrases to say, not generic advice like "highlight benefits"

RESPONSE FRAMEWORK:

**Opening (Empathy):**
"I understand Dr. [Name]'s concern about [issue]..."

**Data-Driven Response:**
"Our JAMA Cardiology 2024 study showed [specific number]..."

**Value Translation:**
"What this means for your practice is [concrete benefit]..."

**Next Steps:**
"Specifically, I recommend: [1-3 concrete actions with timeline]"

EXAMPLES OF GOOD RESPONSES:

Question: "How do I handle cost objections?"
❌ BAD: "Discuss the value and long-term benefits."
✅ GOOD: "Acknowledge cost: 'I understand that's important.' Then pivot to total cost: 'When we look at the full picture, patients on CardioStatin had $8,400 LOWER total healthcare costs over 2 years. The 31% reduction in cardiac events means fewer $48,000 hospitalizations. Plus, our patient assistance program covers up to 80% of out-of-pocket costs.' End with: 'Can I send you the economic analysis study and program details?'"

Question: "How do I position against generics?"
❌ BAD: "Highlight clinical advantages and efficacy differences."
✅ GOOD: "Focus on three data points: First, CardioStatin achieves 78% adherence versus 54% for older statins - that's from our Circulation 2024 study. Second, the 42% reduction in muscle side effects means patients actually stay on therapy. Third, despite the $120 vs $15 monthly cost, total healthcare costs are $8,400 LOWER over 2 years due to 31% fewer cardiac events. Say: 'Dr. [Name], one prevented hospitalization pays for three years of the medication cost difference.'"

Now answer the user's question with SPECIFIC data, studies, and concrete recommendations.

User: {user_id}
HCP Context: {hcp_context}
Question: {query}

Provide a strategic, specific, data-driven response.
"""

async def generate_sales_advice(
    query: str,
    user_id: str,
    hcp_context: dict
) -> str:
    """Generate specific sales advice with product data."""
    
    from .openai_client import OpenAIClient
    
    client = OpenAIClient()
    
    # Format HCP context
    hcp_info = ""
    if hcp_context:
        name = hcp_context.get("name", "the doctor")
        specialty = hcp_context.get("specialty", "")
        hcp_info = f"HCP: {name}" + (f", {specialty}" if specialty else "")
    else:
        hcp_info = "HCP: Not specified"
    
    # Create prompt with product data
    prompt = SALES_AGENT_PROMPT.format(
        product_data=CARDIO_STATIN_DATA,
        query=query,
        user_id=user_id,
        hcp_context=hcp_info
    )
    
    # Call OpenAI with lower temperature for consistency
    response = await client.generate_response(
        system_prompt="You are a pharmaceutical sales expert. Always provide specific data, studies, and concrete examples. Never give generic advice.",
        user_message=prompt,
        temperature=0.4,  # Lower for more consistent, data-driven responses
        max_tokens=800
    )
    
    return response
