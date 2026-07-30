"""
LangGraph Workflow

Workflow:

User Question
      │
      ▼
Question Classifier
      │
      ├──────────────┐
      ▼              ▼
RELATED        UNRELATED
      │              │
      ▼              ▼
 AI Node      Safe Response
      │
      ▼
 Final Response
"""

from langgraph.graph import StateGraph, END

from app.state import AgentState
from app.classifier import classifier
from app.llm import llm
from app.prompts import SAFE_RESPONSE
from app.utils import log_error


def classify_node(state: AgentState) -> AgentState:
    """
    Classify the user's question.
    """

    try:
        state["classification"] = classifier.classify(
            state["question"]
        )

    except Exception as e:
        log_error(f"Classifier Node Error: {e}")

        state["classification"] = "UNRELATED"
        state["error"] = str(e)

    return state


def ai_node(state: AgentState) -> AgentState:
    """
    Generate AI response for related questions.
    """

    try:
        history = state.get("history", [])

        state["response"] = llm.chat(
            user_message=state["question"],
            history=history,
        )

    except Exception as e:
        log_error(f"AI Node Error: {e}")

        state["response"] = (
            "Sorry, I couldn't generate a response."
        )

        state["error"] = str(e)

    return state


def safe_node(state: AgentState) -> AgentState:
    """
    Handle unrelated questions.
    """

    state["response"] = SAFE_RESPONSE

    return state


def route_question(state: AgentState) -> str:
    """
    Decide which node should execute next.
    """

    return "ai" if state["classification"] == "RELATED" else "safe"


# ==========================
# Build LangGraph
# ==========================

builder = StateGraph(AgentState)

builder.add_node("classifier", classify_node)
builder.add_node("ai", ai_node)
builder.add_node("safe", safe_node)

builder.set_entry_point("classifier")

builder.add_conditional_edges(
    "classifier",
    route_question,
    {
        "ai": "ai",
        "safe": "safe",
    },
)

builder.add_edge("ai", END)
builder.add_edge("safe", END)

graph = builder.compile()