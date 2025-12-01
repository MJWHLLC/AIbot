"""Prompt templates and helpers for the Paralegal Assistant persona."""

SYSTEM_PROMPT = (
    "You are a Paralegal AI Assistant working under attorney supervision. "
    "You provide paralegal support and procedures, not legal advice. "
    "Always include the disclaimer: 'I am a paralegal AI assistant working under attorney supervision. "
    "This is not legal advice and requires attorney review.'"
)


def build_document_prompt(doc_type: str, jurisdiction: str, user_text: str) -> str:
    """Build a combined prompt given document type, jurisdiction, and user text."""
    parts = [SYSTEM_PROMPT]
    parts.append(f"Document Type: {doc_type}")
    parts.append(f"Jurisdiction: {jurisdiction}")
    parts.append("Instructions: Follow the paralegal assistant guidelines. Provide checklists, formatting requirements, and items for attorney review.")
    parts.append("User Input:")
    parts.append(user_text)
    return "\n\n".join(parts)
