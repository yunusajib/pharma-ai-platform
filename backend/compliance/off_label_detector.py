"""
Off-Label Promotion Detection System
Multi-layer detection to prevent FDA violations
"""

import re
from typing import Dict, List


class OffLabelDetector:
    """
    Detects off-label promotion attempts using keyword and pattern matching.
    """

    # FDA-approved indications (example for demo)
    APPROVED_INDICATIONS = [
        "hyperlipidemia",
        "high cholesterol",
        "elevated ldl",
        "cardiovascular risk reduction"
    ]

    # Prohibited terms
    OFF_LABEL_KEYWORDS = [
        "off-label",
        "off label",
        "unapproved use",
        "non-approved indication",
        "investigational use"
    ]

    # Implicit off-label patterns
    IMPLICIT_PATTERNS = [
        r"some (?:doctors|physicians|clinicians) (?:use|prescribe|find success)",
        r"might(?:\s+also)? (?:work|help|benefit) (?:for|with)",
        r"can be used for",
        r"doctors have found",
        r"in practice.*works for"
    ]

    # Common off-label conditions (example - would be customized per drug)
    COMMON_OFF_LABEL_CONDITIONS = [
        "migraine",
        "headache prevention",
        "weight loss",
        "pediatric use",
        "children",
        "pregnancy"
    ]

    def detect(self, text: str) -> Dict:
        """
        Detect potential off-label promotion in text.

        Args:
            text: Text to analyze (query or response)

        Returns:
            Dictionary with detection results
        """
        text_lower = text.lower()

        # Check 1: Explicit off-label language
        for keyword in self.OFF_LABEL_KEYWORDS:
            if keyword in text_lower:
                return {
                    "is_violation": True,
                    "violation_type": "explicit_off_label",
                    "detected_text": keyword,
                    "explanation": f"Text contains explicit off-label language: '{keyword}'"
                }

        # Check 2: Implicit patterns
        for pattern in self.IMPLICIT_PATTERNS:
            match = re.search(pattern, text_lower)
            if match:
                return {
                    "is_violation": True,
                    "violation_type": "implicit_off_label",
                    "detected_text": match.group(0),
                    "explanation": f"Text contains implicit off-label suggestion: '{match.group(0)}'"
                }

        # Check 3: Mention of unapproved conditions
        for condition in self.COMMON_OFF_LABEL_CONDITIONS:
            if condition in text_lower:
                # Check if it's being discussed in an approved context
                if not self._is_approved_context(text_lower):
                    return {
                        "is_violation": True,
                        "violation_type": "unapproved_indication",
                        "detected_text": condition,
                        "explanation": f"Discussion of unapproved indication: '{condition}'. Approved uses: {', '.join(self.APPROVED_INDICATIONS)}"
                    }

        # No violations detected
        return {
            "is_violation": False,
            "violation_type": None,
            "detected_text": None,
            "explanation": "No off-label promotion detected"
        }

    def _is_approved_context(self, text: str) -> bool:
        """
        Check if off-label condition is mentioned in an approved context
        (e.g., "not approved for X" is okay)
        """
        approved_phrases = [
            "not approved for",
            "is not indicated for",
            "not fda-approved for",
            "outside approved indications"
        ]

        return any(phrase in text for phrase in approved_phrases)


class ComplianceGuardian:
    """
    Main compliance checking system.
    Coordinates multiple detection layers.
    """

    def __init__(self):
        self.off_label_detector = OffLabelDetector()

    def check_compliance(self, query: str, response: str) -> Dict:
        """
        Comprehensive compliance check on query and response.

        Args:
            query: User's original question
            response: AI-generated response

        Returns:
            Dictionary with compliance status
        """
        # Check query for off-label requests
        query_check = self.off_label_detector.detect(query)

        if query_check["is_violation"]:
            return {
                "status": "BLOCKED",
                "violation_type": query_check["violation_type"],
                "explanation": query_check["explanation"],
                "detected_in": "query"
            }

        # Check response for off-label content
        response_check = self.off_label_detector.detect(response)

        if response_check["is_violation"]:
            return {
                "status": "BLOCKED",
                "violation_type": response_check["violation_type"],
                "explanation": response_check["explanation"],
                "detected_in": "response"
            }

        # All checks passed
        return {
            "status": "APPROVED",
            "violation_type": None,
            "explanation": None,
            "detected_in": None
        }
