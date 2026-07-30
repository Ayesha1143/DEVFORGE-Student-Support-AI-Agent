"""
Question Classifier

This module determines whether a user's question is related
to DEVFORGE internship and technical learning.

Primary Method:
    - LLM Classification (Ollama Cloud)

Fallback:
    - Keyword-based Classification
"""

from app.llm import llm
from app.config import settings
from app.utils import log_error


class QuestionClassifier:
    """
    Handles question classification.
    """

    def __init__(self):
        self.allowed_topics = settings.ALLOWED_TOPICS

    def classify(self, question: str) -> str:
        """
        Returns:
            RELATED
            or
            UNRELATED
        """

        try:
            return llm.classify(question)

        except Exception as e:
            log_error(f"LLM Classification Failed: {e}")

            return self.keyword_fallback(question)

    def keyword_fallback(self, question: str) -> str:
        """
        Keyword-based backup classifier.
        """

        question = question.lower()

        for topic in self.allowed_topics:
            if topic in question:
                return "RELATED"

        return "UNRELATED"


# Singleton instance
classifier = QuestionClassifier()