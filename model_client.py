"""Model client wrapper for calling GitHub-hosted models.

This module intentionally does not embed secrets. It reads the model API token
from the environment variable `GITHUB_MODEL_API_TOKEN` and the model name from
`GITHUB_MODEL_NAME`.

If you do not provide a token, the client will run in a safe local "mock"
mode so you can test the app without contacting external services.
"""
from __future__ import annotations

import os
import json
import requests
from typing import Optional


class ModelClient:
    def __init__(self, api_token: Optional[str] = None, model_name: Optional[str] = None):
        self.api_token = api_token or os.environ.get("GITHUB_MODEL_API_TOKEN")
        self.model_name = model_name or os.environ.get("GITHUB_MODEL_NAME")

    def _call_github_model(self, prompt: str) -> str:
        """Placeholder for actual GitHub models API call.

        NOTE: Implement actual API integration according to GitHub's models
        API documentation. Do not commit tokens to source control; provide
        them in environment variables or a secrets manager.
        """
        assert self.api_token, "GITHUB_MODEL_API_TOKEN is required for real API calls"
        assert self.model_name, "GITHUB_MODEL_NAME is required for real API calls"

        # Example: POST to a hypothetical GitHub models endpoint (this is a placeholder)
        url = f"https://api.github.com/models/{self.model_name}/invoke"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }
        payload = {"input": prompt}
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        # This depends on actual API shape
        return data.get("output") or json.dumps(data)

    def generate(self, prompt: str) -> str:
        """Generate a response for the given prompt.

        If no token is provided, return a deterministic mock response for testing.
        """
        if not self.api_token:
            # Mock behavior for local testing
            return (
                "[MOCK RESPONSE] This is a mocked paralegal assistant response. "
                "Provide a real GITHUB_MODEL_API_TOKEN and GITHUB_MODEL_NAME to enable live calls.\n\n"
                "Prompt summary:\n" + (prompt[:200] + "..." if len(prompt) > 200 else prompt)
            )

        # Real call path
        return self._call_github_model(prompt)
