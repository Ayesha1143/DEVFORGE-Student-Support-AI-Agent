"""
Main FastAPI Application

Entry point for the DEVFORGE Student Support AI Agent.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

from app.config import settings
from app.models import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    HomeResponse,
)
from app.agent import agent


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="DEVFORGE Student Support AI Agent powered by LangGraph and Ollama Cloud."
)


# -------------------------------
# CORS
# -------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------
# Static Files & Templates
# -------------------------------

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


# -------------------------------
# Home Page
# -------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Render the chat interface.
    """
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": settings.APP_NAME,
        },
    )


# -------------------------------
# Health Check
# -------------------------------

@app.get("/health", response_model=HealthResponse)
async def health():
    """
    Check API health.
    """
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
    )


# -------------------------------
# Chat Endpoint
# -------------------------------

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the AI agent.
    """

    try:

        result = agent.chat(
            question=request.message,
            history=request.history,
        )

        return ChatResponse(
            response=result["response"],
            classification=result["classification"],
            response_time=result["response_time"],
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# -------------------------------
# API Information
# -------------------------------

@app.get("/info", response_model=HomeResponse)
async def info():
    """
    Basic API information.
    """

    return HomeResponse(
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="DEVFORGE Student Support AI Agent",
    )