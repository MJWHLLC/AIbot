"""GitHub Models API client for real Azure inference endpoint integration."""
import os
import json
import logging
from typing import Optional
import requests

logger = logging.getLogger(__name__)


class ModelClient:
    """Client for calling GitHub-hosted models via Azure inference endpoint."""

    def __init__(self):
        """Initialize with GitHub Models API token and model name."""
        self.api_token = os.environ.get("GITHUB_MODEL_API_TOKEN")
        self.model_name = os.environ.get("GITHUB_MODEL_NAME", "gpt-4o-mini")
        self.endpoint = "https://models.inference.ai.azure.com/chat/completions"
        
        if not self.api_token:
            logger.warning("GITHUB_MODEL_API_TOKEN not set; will use mock responses for testing")

    def generate(self, prompt: str, system_role: Optional[str] = None) -> str:
        """
        Generate a response using the GitHub model.
        
        Args:
            prompt: The user prompt/question
            system_role: Optional system role message. If not included in prompt, used here.
            
        Returns:
            Model response text
        """
        if not self.api_token:
            return self._mock_response(prompt)

        try:
            return self._call_github_model(prompt, system_role)
        except Exception as exc:
            logger.error(f"GitHub Models API error: {exc}; falling back to mock")
            return self._mock_response(prompt)

    def _call_github_model(self, prompt: str, system_role: Optional[str] = None) -> str:
        """
        Make actual HTTP call to GitHub Models API endpoint.
        
        Args:
            prompt: User message/prompt
            system_role: System message (paralegal role, context, etc.)
            
        Returns:
            Response text from model
            
        Raises:
            Exception: If API call fails
        """
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

        messages = []
        
        # If system_role is provided separately, add it as a system message
        if system_role:
            messages.append({
                "role": "system",
                "content": system_role
            })
        
        # Add user prompt
        messages.append({
            "role": "user",
            "content": prompt
        })

        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2048,
            "top_p": 1.0
        }

        logger.info(f"Calling GitHub Models API endpoint: {self.endpoint}")
        logger.info(f"Using model: {self.model_name}")

        response = requests.post(
            self.endpoint,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Extract message content from response
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        
        raise ValueError(f"Unexpected API response format: {result}")

    def _mock_response(self, prompt: str) -> str:
        """
        Return a mock response for testing without API token.
        
        Args:
            prompt: User prompt
            
        Returns:
            Simulated paralegal response
        """
        if "complaint" in prompt.lower():
            return """[MOCK RESPONSE - DEVELOP ONLY]

FEDERAL CIVIL COMPLAINT

I. JURISDICTION AND VENUE
1. This Court has subject matter jurisdiction pursuant to 28 U.S.C. § 1331 (federal question).
2. Venue is proper in this District under 28 U.S.C. § 1391.

II. PARTIES
1. Plaintiff [Your Name], a citizen of [State], brings this action.
2. Defendant [Defendant Name], a citizen of [State], is the Defendant.

III. FACTS
[Insert factual allegations supporting your claims]

IV. LEGAL CLAIMS
[Insert claims with statutory citations]

V. PRAYER FOR RELIEF
Plaintiff respectfully requests relief as follows:
- [Relief 1]
- [Relief 2]
- Costs and attorneys' fees

⚠️ DISCLAIMER: This is a template only. Requires attorney review before filing.
"""
        
        elif "discovery" in prompt.lower():
            return """[MOCK RESPONSE - DEVELOP ONLY]

INTERROGATORIES TO DEFENDANT

Pursuant to Fed. R. Civ. P. 33, Plaintiff requests that Defendant answer the following interrogatories within 30 days:

1. Identify all documents relating to [subject matter].
2. State the factual basis for each denial in your answer.
3. Identify all persons with knowledge of [topic].

REQUESTS FOR PRODUCTION OF DOCUMENTS

Pursuant to Fed. R. Civ. P. 34, Plaintiff requests production of:

1. All emails and communications regarding [topic]
2. All internal reports or analyses concerning [topic]
3. All witness statements or declarations

⚠️ DISCLAIMER: This is a template only. Requires attorney review before serving.
"""
        
        elif "deadline" in prompt.lower() or "rule 6" in prompt.lower():
            return """[MOCK RESPONSE - DEVELOP ONLY]

FEDERAL RULE OF CIVIL PROCEDURE 6 - TIMING DEADLINES

1. CALCULATING TIME:
   - Exclude the day the event happens
   - Include the last day if it's a weekday
   - If deadline falls on weekend/holiday, next business day counts as the deadline

2. COMMON DEADLINES:
   - Response to pleading: 21 days
   - Motion response: 14 days
   - Discovery response: 30 days (interrogatories, requests for production)
   - Deposition notice: 14 days (except expert witnesses: 21 days)

EXAMPLE: If Complaint served Monday, Jan 8, Response due by 5 PM Friday, Jan 29.

⚠️ DISCLAIMER: Verify applicable local rules and any court orders modifying these deadlines.
"""
        
        else:
            return f"""[MOCK RESPONSE - DEVELOP ONLY]

Your Query: {prompt[:100]}...

This is a mock response used when GITHUB_MODEL_API_TOKEN environment variable is not configured.

To use real GitHub Models API:
1. Set GITHUB_MODEL_API_TOKEN environment variable with your GitHub token
2. Ensure token has 'read:models' permission
3. Restart the application

Real API responses will provide:
- Document drafting assistance
- Legal research guidance
- Procedure and deadline analysis
- Case management support

All responses require attorney review before use.

⚠️ DISCLAIMER: This is a template only. All work requires attorney supervision and review.
"""
