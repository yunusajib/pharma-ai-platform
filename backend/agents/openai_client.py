"""
OpenAI API Client
Handles all interactions with OpenAI API
"""

import os
from typing import Dict, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class OpenAIClient:
    """
    Wrapper for OpenAI API calls.
    """

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables")

        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"  # Using mini for cost efficiency in demo

    async def generate_response(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> str:
        """
        Generate response from OpenAI.

        Args:
            system_prompt: System instructions for the model
            user_message: User's question/input
            temperature: Randomness (0.0 = deterministic, 1.0 = creative)
            max_tokens: Maximum response length

        Returns:
            Generated text response
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )

            return response.choices[0].message.content

        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

# Singleton instance
_client_instance = None

def get_openai_client() -> OpenAI:
    """
    Get or create OpenAI client instance (singleton pattern).
    
    Returns:
        OpenAI: Configured OpenAI client
    """
    global _client_instance
    if _client_instance is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        _client_instance = OpenAI(api_key=api_key)
    return _client_instance
