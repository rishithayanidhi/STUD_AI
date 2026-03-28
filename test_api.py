"""Quick API test"""
import requests
import json

try:
    # Test health endpoint
    print("Testing health endpoint...")
    r = requests.get("http://localhost:8000/health", timeout=3)
    print(f"✓ Health: {r.json()}")
    
    # Test ticket processing
    print("\nTesting ticket endpoint...")
    r = requests.post("http://localhost:8000/ticket", json={
        "issue": "Production API failing with 500 error affecting payments"
    }, timeout=5)
    
    if r.status_code == 200:
        result = r.json()
        print(f"✓ Ticket processed")
        print(f"  Category: {result['classification']['category']}")
        print(f"  Priority: {result['classification']['priority']}")
        print(f"  Team: {result['classification']['team']}")
        print(f"  Actions executed: {len(result['actions_executed'])}")
        print(f"  Similar tickets found: {len(result['similar_past_tickets'])}")
    else:
        print(f"✗ Error {r.status_code}: {r.text}")
        
except Exception as e:
    print(f"✗ Error: {e}")
    print("\nMake sure the API is running:")
    print("python run_server.py")
