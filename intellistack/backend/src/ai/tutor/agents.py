"""
Stub for legacy tutor agent interface.
The active AI tutor is SocraticTutorAgent in src/ai/chatkit/agent.py (Gemini-based).
These stubs exist to keep the legacy tutor service importable without openai-agents.
"""

from typing import Any, Dict


def create_tutor_agent(stage_level: int) -> Dict[str, Any]:
    """Stub — legacy OpenAI-agents tutor, superseded by SocraticTutorAgent."""
    return {"stage_level": stage_level}


async def run_tutor_conversation(
    agent: Any,
    content: str,
    session_id: str = "",
    db_path: str = "",
) -> Dict[str, Any]:
    """Stub — legacy OpenAI-agents tutor, superseded by SocraticTutorAgent."""
    return {
        "final_output": (
            "The legacy tutor endpoint is not active. "
            "Please use the ChatKit AI assistant instead."
        )
    }
