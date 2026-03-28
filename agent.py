"""
Autonomous Ops Agent - Using Ollama for reasoning (local LLM inference).
Classifies tickets and suggests actions.
"""

import os
import json
from typing import Optional

try:
    from ollama import chat
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    import requests


def get_ollama_config():
    """Get Ollama configuration from environment."""
    ollama_model = os.getenv("OLLAMA_MODEL", "mistral")
    
    if OLLAMA_AVAILABLE:
        print(f"✓ Ollama chat API imported successfully (model: {ollama_model})")
    else:
        print(f"⚠️  Ollama chat API not available, will use requests fallback")
    
    return ollama_model


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


def classify_ticket_with_ai(ollama_model: str, issue: str) -> dict:
    """Use Ollama (local LLM) to classify ticket using chat API."""
    
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
        # Use chat API if available
        if OLLAMA_AVAILABLE:
            response = chat(
                model=ollama_model,
                messages=[{'role': 'user', 'content': prompt}],
            )
            response_text = response.message.content.strip()
        else:
            # Fallback to requests API
            import requests
            ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
            api_response = requests.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.3,
                },
                timeout=30
            )
            response_text = api_response.json()["response"].strip()
        
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
        print(f"Ollama error: {e}, using mock classification")
        return get_mock_classification(issue)


def process_ticket(issue: str) -> dict:
    """Main entry point: classify and prepare decision."""
    
    # Get Ollama model
    ollama_model = get_ollama_config()
    
    # Classify the ticket
    classification = classify_ticket_with_ai(ollama_model, issue)
    
    # Add original issue to the decision
    decision = {
        "issue": issue,
        **classification
    }
    
    return decision
