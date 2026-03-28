"""
FastAPI application for the autonomous ops demo.
Main entry point for the demo.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json

from agent import process_ticket
from tools import executor
from memory import memory


app = FastAPI(
    title="Autonomous Ops Demo",
    description="Ticket → AI Decision → Execution → Memory",
    version="0.1.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TicketRequest(BaseModel):
    """Incoming ticket data."""
    issue: str
    context: Optional[str] = None


class TicketResponse(BaseModel):
    """Response with decision and execution log."""
    issue: str
    classification: dict
    actions_executed: list
    similar_past_tickets: list
    execution_log: list


@app.get("/health")
async def health():
    """Health check."""
    return {"status": "ok"}


@app.post("/ticket", response_model=TicketResponse)
async def create_ticket(request: TicketRequest):
    """
    Submit a ticket for autonomous processing.
    
    1. AI classifies the ticket
    2. Tools execute actions
    3. Memory stores for learning
    4. Returns full decision trace
    """
    
    if not request.issue or len(request.issue.strip()) < 5:
        raise HTTPException(status_code=400, detail="Issue must be at least 5 characters")
    
    # Step 1: AI reasoning
    decision = process_ticket(request.issue)
    
    # Step 2: Execute actions
    execution_result = executor.execute(decision)
    
    # Step 3: Store for future learning
    memory.store_ticket(request.issue, decision)
    
    # Step 4: Find similar past tickets (learning)
    similar = memory.find_similar_tickets(request.issue, n_results=2)
    
    return TicketResponse(
        issue=request.issue,
        classification={
            "category": decision.get("category"),
            "priority": decision.get("priority"),
            "team": decision.get("team"),
            "confidence": decision.get("confidence", 0.0),
            "suggested_action": decision.get("suggested_action")
        },
        actions_executed=execution_result["executed"],
        similar_past_tickets=similar,
        execution_log=execution_result["action_log"]
    )


@app.get("/memory/tickets")
async def get_all_tickets():
    """Retrieve all stored tickets."""
    return {"tickets": memory.tickets}


@app.get("/memory/search")
async def search_tickets(query: str):
    """Search for similar tickets."""
    if not query:
        raise HTTPException(status_code=400, detail="Query required")
    
    results = memory.find_similar_tickets(query, n_results=5)
    return {"query": query, "results": results}


@app.get("/stats")
async def get_stats():
    """Get system statistics and memory backend info."""
    stats = memory.get_stats()
    return {
        "status": "running",
        "memory": stats,
        "backend": "postgres" if memory.use_postgres else "json",
        "database": memory.conn.get_dsn_parameters() if memory.use_postgres and memory.conn else None
    }


@app.get("/")
async def root():
    """API info and quick start."""
    return {
        "app": "Autonomous Ops Demo",
        "endpoints": {
            "POST /ticket": "Submit and process a ticket",
            "GET /memory/tickets": "View all stored tickets",
            "GET /memory/search": "Search for similar tickets",
            "GET /stats": "View system stats and memory backend",
            "GET /health": "Health check"
        },
        "quick_start": {
            "curl": 'curl -X POST "http://localhost:8000/ticket" -H "Content-Type: application/json" -d \'{"issue": "Production API failing"}\'',
            "python": "import requests; requests.post('http://localhost:8000/ticket', json={'issue': 'Your issue here'})"
        }
    }


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Autonomous Ops Demo API...")
    print("📖 API docs: http://localhost:8000/docs")
    print("🎯 Try: POST /ticket with {\"issue\": \"...\"}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
