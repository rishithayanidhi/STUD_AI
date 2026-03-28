"""
Autonomous Ops Agent - Using Ollama for reasoning (local LLM inference).
Classifies tickets and suggests actions.
"""

import os
import json
import requests
from typing import Optional


def get_ollama_client():
    """Initialize Ollama client (local LLM)."""
    ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
    ollama_model = os.getenv("OLLAMA_MODEL", "llama3")
    
    # Test connection
    try:
        response = requests.get(f"{ollama_url}/api/tags", timeout=2)
        if response.status_code == 200:
            print(f"✓ Ollama connected at {ollama_url}")
            return {"url": ollama_url, "model": ollama_model}
    except requests.exceptions.RequestException:
        print(f"⚠️  Ollama not available at {ollama_url}")
    
    return None


def get_mock_classification(issue: str) -> dict:
    """Fallback: mock classification if OpenAI unavailable."""
    issue_lower = issue.lower()
    
    priority = "High" if any(x in issue_lower for x in ["failing", "500", "down", "outage"]) else "Medium"
    
    if "payment" in issue_lower or "billing" in issue_lower:
        team = "Backend / Payments"
    elif "api" in issue_lower or "server" in issue_lower:
        team = "Backend"
    elif "ui" in issue_lower or "frontend" in issue_lower:
        team = "Frontend"
    else:
        team = "Operations"
    
    return {
        "category": "Incident" if priority == "High" else "Request",
        "priority": priority,
        "team": team,
        "confidence": 0.75,
        "suggested_action": f"Investigate and page {team} team"
    }


def classify_ticket_with_ai(client: Optional[dict], issue: str) -> dict:
    """Use Ollama (local LLM) to classify ticket."""
    
    if not client:
        return get_mock_classification(issue)
    
    prompt = f"""You are an IT operations classification system. Analyze this ticket and respond ONLY with valid JSON.

Issue: {issue}

Respond with ONLY this JSON structure (no markdown, no explanation):
{{
    "category": "Incident|Request|Change|Problem",
    "priority": "Critical|High|Medium|Low",
    "team": "Backend|Frontend|DevOps|Operations",
    "confidence": 0.0_to_1.0,
    "suggested_action": "brief action description"
}}

Only return JSON, nothing else."""
    
    try:
        response = requests.post(
            f"{client['url']}/api/generate",
            json={
                "model": client['model'],
                "prompt": prompt,
                "stream": False,
                "temperature": 0.3,
            },
            timeout=30
        )
        
        if response.status_code == 200:
            response_text = response.json()["response"].strip()
            
            # Try to extract JSON if wrapped in markdown
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(response_text)
            return result
    
    except json.JSONDecodeError:
        print(f"JSON parse error, falling back to mock classification")
        return get_mock_classification(issue)
    except Exception as e:
        print(f"Ollama error: {e}, using mock")
        return get_mock_classification(issue)


def process_ticket(issue: str) -> dict:
    """Main entry point: classify and prepare decision."""
    
    # Get Ollama client (None if not available)
    client = get_ollama_client()
    
    # Classify the ticket
    classification = classify_ticket_with_ai(client, issue)
    
    # Add original issue to the decision
    decision = {
        "issue": issue,
        **classification
    }
    
    return decision
