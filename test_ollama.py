#!/usr/bin/env python
"""
Test Ollama integration with local LLM inference.
"""

import requests
import json
import sys

# Test connection
print("Testing Ollama connection...")
try:
    response = requests.get("http://localhost:11434/api/tags", timeout=5)
    if response.status_code == 200:
        models = response.json().get("models", [])
        print(f"✓ Ollama is running")
        print(f"  Available models: {len(models)}")
        if models:
            for m in models:
                print(f"    - {m.get('name')}")
        else:
            print("  ⚠️  No models available. Run: docker exec ollama ollama pull llama3")
    else:
        print(f"✗ Ollama returned status {response.status_code}")
        sys.exit(1)
except requests.exceptions.RequestException as e:
    print(f"✗ Cannot connect to Ollama at http://localhost:11434")
    print(f"  Error: {e}")
    print("\n  Start Ollama with:")
    print("    docker run -d -p 11434:11434 ollama/ollama")
    sys.exit(1)

# Test classification
print("\nTesting classification...")

test_tickets = [
    "Production application is down - 500 errors",
    "Update user profile page styling",
    "Add two-factor authentication feature",
    "Database slow queries on reporting dashboard"
]

for ticket in test_tickets:
    print(f"\n  Ticket: {ticket}")
    
    prompt = f"""You are an IT operations classification system. Analyze this ticket and respond ONLY with valid JSON.

Issue: {ticket}

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
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
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
            
            try:
                result = json.loads(response_text)
                print(f"    ✓ {result['category']} - {result['priority']} - {result['team']}")
                print(f"      Confidence: {result['confidence']}")
            except json.JSONDecodeError as e:
                print(f"    ✗ JSON parse error: {e}")
                print(f"    Response: {response_text[:100]}...")
        else:
            print(f"    ✗ Error {response.status_code}")
    except requests.exceptions.Timeout:
        print(f"    ✗ Request timeout (model might be loading for first time)")
    except Exception as e:
        print(f"    ✗ Error: {e}")

print("\n✓ Test complete!")
