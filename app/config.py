"""
Application Configuration

This module loads all environment variables required by the
DEVFORGE Student Support AI Agent.

Never hardcode API keys in the project.
"""

import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv(dotenv_path=".env")


class Config:
    """
    Application configuration class.
    """

    # ==========================
    # Ollama Cloud Configuration
    # ==========================
    OLLAMA_API_KEY: str | None = os.getenv("OLLAMA_API_KEY")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen3")

    # ==========================
    # FastAPI Configuration
    # ==========================
    APP_NAME: str = "DEVFORGE Student Support AI Agent"
    APP_VERSION: str = "1.0.0"

    # ==========================
    # Allowed Technical Topics
    # ==========================
    ALLOWED_TOPICS = [
        "ai",
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "python",
        "fastapi",
        "langchain",
        "langgraph",
        "github",
        "git",
        "api",
        "deployment",
        "render",
        "koyeb",
        "ollama",
        "qwen",
        "project",
        "assignment",
        "internship",
        "devforge",
        "web development",
        "backend",
    ]

    @staticmethod
    def validate() -> None:
        """
        Validate required environment variables.
        """

        if not Config.OLLAMA_API_KEY:
            raise ValueError(
                "OLLAMA_API_KEY is missing. Please add it to your .env file."
            )

        if not Config.OLLAMA_MODEL:
            raise ValueError(
                "OLLAMA_MODEL is missing. Please add it to your .env file."
            )


# Global config object
settings = Config()

# Validate configuration on startup
settings.validate()