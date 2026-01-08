"""
Agent Orchestration System
Coordinates multiple agents to process user queries
"""

import time
from typing import Dict, List
from agents.openai_client import OpenAIClient
from prompts.sales_agent import get_sales_agent_prompt
from compliance.off_label_detector import ComplianceGuardian


class AgentOrchestrator:
    """
    Orchestrates the multi-agent system.
    Routes queries to appropriate agents and enforces compliance.
    """

    def __init__(self):
        self.openai_client = OpenAIClient()
        self.compliance_guardian = ComplianceGuardian()

    async def process_query(
        self,
        query: str,
        user_id: str,
        hcp_context: Dict = None
    ) -> Dict:
        """
        Process a user query through the multi-agent system.

        Args:
            query: User's question
            user_id: ID of the user asking
            hcp_context: Context about the HCP (optional)

        Returns:
            Complete response with compliance status
        """
        start_time = time.time()
        agents_used = []

        # Step 1: Check query for compliance violations
        initial_compliance = self.compliance_guardian.check_compliance(
            query, "")

        if initial_compliance["status"] == "BLOCKED":
            # Query itself is non-compliant
            return {
                "response": self._generate_educational_block_message(
                    initial_compliance["violation_type"],
                    initial_compliance["explanation"]
                ),
                "agents_used": ["compliance_guardian"],
                "compliance_status": {
                    "status": "BLOCKED",
                    "violation_type": initial_compliance["violation_type"],
                    "explanation": initial_compliance["explanation"]
                },
                "response_time_seconds": round(time.time() - start_time, 3)
            }

        # Step 2: Determine which agent should handle this
        agent_type = self._determine_agent_type(query)
        agents_used.append(f"{agent_type}_agent")

        # Step 3: Generate response using appropriate agent
        if agent_type == "sales":
            response = await self._call_sales_agent(query, hcp_context)
        else:
            # For MVP, all queries go to sales agent
            response = await self._call_sales_agent(query, hcp_context)

        # Step 4: Compliance Guardian reviews the response
        agents_used.append("compliance_guardian")
        final_compliance = self.compliance_guardian.check_compliance(
            query, response)

        if final_compliance["status"] == "BLOCKED":
            # Response generated off-label content
            return {
                "response": self._generate_educational_block_message(
                    final_compliance["violation_type"],
                    final_compliance["explanation"]
                ),
                "agents_used": agents_used,
                "compliance_status": {
                    "status": "BLOCKED",
                    "violation_type": final_compliance["violation_type"],
                    "explanation": final_compliance["explanation"]
                },
                "response_time_seconds": round(time.time() - start_time, 3)
            }

        # Step 5: Response approved - return to user
        return {
            "response": response,
            "agents_used": agents_used,
            "compliance_status": {
                "status": "APPROVED",
                "violation_type": None,
                "explanation": None
            },
            "response_time_seconds": round(time.time() - start_time, 3)
        }

    def _determine_agent_type(self, query: str) -> str:
        """
        Determine which agent should handle the query.

        For MVP: All queries go to sales agent.
        In full version: Route to medical, compliance, etc. based on content.
        """
        # Simple keyword-based routing for now
        medical_keywords = ["mechanism",
                            "interaction", "dosing", "pharmacokinetic"]

        query_lower = query.lower()

        for keyword in medical_keywords:
            if keyword in query_lower:
                return "medical"  # Would route to medical agent in full version

        return "sales"

    async def _call_sales_agent(self, query: str, hcp_context: Dict = None) -> str:
        """
        Call the Sales Agent to generate strategic selling advice.
        """
        # Get the full prompt with context
        full_prompt = get_sales_agent_prompt(query, hcp_context)

        # Generate response using OpenAI
        response = await self.openai_client.generate_response(
            system_prompt=full_prompt,
            user_message=query,
            temperature=0.7,  # Balanced creativity
            max_tokens=400    # Concise responses
        )

        return response

    def _generate_educational_block_message(
        self,
        violation_type: str,
        explanation: str
    ) -> str:
        """
        Generate educational message when content is blocked.
        Turns compliance violations into teaching moments.
        """
        base_message = f"""⚠️ **COMPLIANCE ALERT**

This request was blocked to protect you from regulatory risk.

**Why this was blocked:**
{explanation}

**What you can say instead:**
"Our drug is FDA-approved for the treatment of hyperlipidemia in adults. For questions about other potential applications, I'd be happy to connect you with our Medical Science Liaison team who can provide published clinical data."

**Learn More:**
- FDA regulations on promotional activities (21 CFR 202.1)
- How to handle off-label questions from HCPs
- Compliant ways to discuss competitor products

**Important:** This interaction has been logged for training purposes. There is no penalty for asking questions—we want you to learn!
"""

        return base_message
