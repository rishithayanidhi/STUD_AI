"""
Autonomous Ops Agent - Using Ollama for reasoning (local LLM inference).
Classifies tickets and suggests actions.
Dynamic configuration from environment variables.
"""

import os
import json
import requests
from typing import Optional


# Configuration loaded from environment
CONFIG = {
    "ollama": {
        "url": os.getenv("OLLAMA_URL", "http://localhost:11434"),
        "model": os.getenv("OLLAMA_MODEL", "llama3"),
        "temperature": float(os.getenv("OLLAMA_TEMPERATURE", "0.3")),
        "timeout": int(os.getenv("OLLAMA_TIMEOUT", "30")),
    },
    "classification": {
        "priority_keywords": {
            "Critical": os.getenv("CRITICAL_KEYWORDS", "failing,500,down,outage,critical,emergency").split(","),
            "High": os.getenv("HIGH_KEYWORDS", "error,bug,issue,broken").split(","),
            "Medium": os.getenv("MEDIUM_KEYWORDS", "slow,performance,degraded").split(","),
            "Low": os.getenv("LOW_KEYWORDS", "feature,enhancement,improvement").split(","),
        },
        "team_assignments": {
            "Backend / Payments": os.getenv("PAYMENTS_KEYWORDS", "payment,billing,transaction,invoice").split(","),
            "Backend": os.getenv("BACKEND_KEYWORDS", "api,server,database,service").split(","),
            "Frontend": os.getenv("FRONTEND_KEYWORDS", "ui,page,layout,button,styling").split(","),
            "DevOps": os.getenv("DEVOPS_KEYWORDS", "deploy,infrastructure,kubernetes,docker,ci/cd").split(","),
            "Operations": os.getenv("OPERATIONS_KEYWORDS", "monitoring,alert,log,metric").split(","),
        },
        "default_team": os.getenv("DEFAULT_TEAM", "Operations"),
        "default_confidence": float(os.getenv("DEFAULT_CONFIDENCE", "0.75")),
    }
}


def get_ollama_client():
    """Initialize Ollama client (local LLM)."""
    url = CONFIG["ollama"]["url"]
    model = CONFIG["ollama"]["model"]
    
    # Test connection
    try:
        response = requests.get(f"{url}/api/tags", timeout=2)
        if response.status_code == 200:
            print(f"✓ Ollama connected at {url} (model: {model})")
            return {"url": url, "model": model}
    except requests.exceptions.RequestException:
        print(f"⚠️  Ollama not available at {url}")
    
    return None


def get_mock_classification(issue: str) -> dict:
    """Fallback: mock classification based on configuration rules."""
    issue_lower = issue.lower()
    
    # Determine priority based on keywords
    priority = "Medium"  # Default
    for level in ["Critical", "High", "Low"]:
        keywords = CONFIG["classification"]["priority_keywords"].get(level, [])
        if any(keyword.strip().lower() in issue_lower for keyword in keywords):
            priority = level
            break
    
    # Determine team based on keywords
    team = CONFIG["classification"]["default_team"]
    for team_name, keywords in CONFIG["classification"]["team_assignments"].items():
        if any(keyword.strip().lower() in issue_lower for keyword in keywords):
            team = team_name
            break
    
    return {
        "category": "Incident" if priority in ["Critical", "High"] else "Request",
        "priority": priority,
        "team": team,
        "confidence": CONFIG["classification"]["default_confidence"],
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
                "temperature": CONFIG["ollama"]["temperature"],
            },
            timeout=CONFIG["ollama"]["timeout"]
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
    
    # Fallback for non-200 responses
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
