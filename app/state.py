"""
State Definition

This module defines the shared state used by the LangGraph workflow.
Each node in the graph reads from and writes to this state.
"""

from typing import TypedDict, List, Dict, Optional


class AgentState(TypedDict):
    """
    Shared state for the DEVFORGE Student Support AI Agent.
    """

    # Current user question
    question: str

    # Classification result
    # Expected values:
    # RELATED
    # UNRELATED
    classification: str

    # Final AI response
    response: str

    # Conversation history
    history: List[Dict[str, str]]

    # Optional error message
    error: Optional[str]