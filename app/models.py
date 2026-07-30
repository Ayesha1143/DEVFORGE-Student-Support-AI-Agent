"""
Pydantic models used throughout the application.

These models validate API requests and responses.
"""

from typing import List, Dict

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Incoming chat request.
    """

    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Student question"
    )

    history: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Conversation history"
    )


class ChatResponse(BaseModel):
    """
    Chat response returned by the AI agent.
    """

    response: str
    classification: str
    response_time: float


class HealthResponse(BaseModel):
    """
    Health check response.
    """

    status: str
    version: str


class ErrorResponse(BaseModel):
    """
    Standard error response.
    """

    error: str


class HomeResponse(BaseModel):
    """
    API information response.
    """

    app_name: str
    version: str
    description: str