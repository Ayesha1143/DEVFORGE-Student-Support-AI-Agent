"""
AI Agent

This module provides a simple interface for interacting
with the LangGraph workflow.
"""

from app.graph import graph
from app.state import AgentState
from app.utils import current_timestamp, response_time, log_info


class StudentSupportAgent:
    """
    DEVFORGE Student Support AI Agent.
    """

    def __init__(self):
        self.graph = graph

    def chat(
        self,
        question: str,
        history: list | None = None,
    ) -> dict:
        """
        Process a user question through the LangGraph workflow.

        Args:
            question: User input.
            history: Previous conversation history.

        Returns:
            Dictionary containing the final response.
        """

        if history is None:
            history = []

        start = current_timestamp()

        state: AgentState = {
            "question": question,
            "classification": "",
            "response": "",
            "history": history,
            "error": None,
        }

        result = self.graph.invoke(state)

        elapsed = response_time(start)

        log_info(f"Response generated in {elapsed} seconds.")

        return {
            "question": result["question"],
            "classification": result["classification"],
            "response": result["response"],
            "response_time": elapsed,
        }


# Singleton instance
agent = StudentSupportAgent()