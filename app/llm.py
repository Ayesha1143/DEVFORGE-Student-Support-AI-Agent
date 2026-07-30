"""
LLM integration for the DEVFORGE Student Support AI Agent.

This module communicates with Ollama Cloud using the official
Python client.
"""

from typing import List, Dict

from ollama import Client

from app.config import settings
from app.prompts import SYSTEM_PROMPT, CLASSIFIER_PROMPT
from app.utils import log_error


class OllamaLLM:
    """
    Handles communication with Ollama Cloud.
    """

    def __init__(self) -> None:
        self.client = Client(
            host="https://ollama.com",
            headers={
                "Authorization": f"Bearer {settings.OLLAMA_API_KEY}"
            },
        )

        self.model = settings.OLLAMA_MODEL

    def _call_ollama(self, messages: List[Dict[str, str]]) -> str:
        """
        Send messages to Ollama Cloud and return the response.
        """

        response = self.client.chat(
            model=self.model,
            messages=messages,
        )

        return response["message"]["content"].strip()

    def chat(
        self,
        user_message: str,
        history: List[Dict[str, str]] | None = None,
    ) -> str:
        """
        Generate a normal chatbot response.
        """

        if history is None:
            history = []

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

        messages.extend(history)

        messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        try:
            return self._call_ollama(messages)

        except Exception as e:
            log_error(f"Ollama Chat Error: {e}")

            return (
                "Sorry, I couldn't generate a response at the moment. "
                "Please try again later."
            )

    def classify(self, question: str) -> str:
        """
        Classify a question as RELATED or UNRELATED.
        """

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a classifier. "
                    "Return only one word: RELATED or UNRELATED."
                ),
            },
            {
                "role": "user",
                "content": CLASSIFIER_PROMPT.format(
                    question=question
                ),
            },
        ]

        try:
            result = self._call_ollama(messages).upper().strip()

            if result in ("RELATED", "UNRELATED"):
                return result

            return "UNRELATED"

        except Exception as e:
            log_error(f"Ollama Classification Error: {e}")

            raise


# Singleton instance
llm = OllamaLLM()