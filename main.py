"""
Main FastAPI Application

Entry point for the DEVFORGE Student Support AI Agent.
"""

import traceback

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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
    description="DEVFORGE Student Support AI Agent powered by LangGraph and Ollama Cloud.",
)


# ===================================================
# GLOBAL EXCEPTION HANDLER (Debugging)
# ===================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print("\n========== UNHANDLED EXCEPTION ==========")
    traceback.print_exc()
    print("=========================================\n")

    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc)
        },
    )


# ===================================================
# CORS
# ===================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===================================================
# Static Files
# ===================================================

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


# ===================================================
# HOME
# ===================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": settings.APP_NAME,
        },
    )


# ===================================================
# HEALTH
# ===================================================

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
    }


# ===================================================
# INFO
# ===================================================

@app.get("/info")
async def info():
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "DEVFORGE Student Support AI Agent",
    }


# ===================================================
# CHAT
# ===================================================

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

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
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
