"""Test the new /stats endpoint"""
import requests

try:
    print("Testing /stats endpoint...")
    r = requests.get("http://localhost:8000/stats", timeout=3)
    
    if r.status_code == 200:
        stats = r.json()
        print(f"\n✓ System Stats:")
        print(f"  Backend: {stats['backend']}")
        print(f"  Status: {stats['status']}")
        print(f"  Storage: {stats['memory'].get('storage', 'unknown')}")
        print(f"  Total Tickets: {stats['memory'].get('total_tickets', 0)}")
        
        if stats['backend'] == 'postgres':
            print(f"\n🎉 PostgreSQL is CONNECTED!")
        else:
            print(f"\nℹ️  Using JSON fallback (PostgreSQL not configured)")
    else:
        print(f"✗ Error {r.status_code}: {r.text}")
        
except Exception as e:
    print(f"✗ Error: {e}")
    print("\nMake sure the API is running:")
    print("python run_server.py")
