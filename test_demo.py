"""
Demo test script - Run this to verify the autonomous ops flow end-to-end.
"""

import json
import time
from agent import process_ticket
from tools import executor
from memory import memory


def demo_flow():
    """Run complete demo flow."""
    
    print("\n" + "="*70)
    print("🤖 AUTONOMOUS OPS DEMO - END-TO-END FLOW")
    print("="*70)
    
    # Test tickets
    test_tickets = [
        "Production API failing with 500 error affecting payments",
        "Database replication lag detected on primary cluster",
        "Website responding slowly during peak hours"
    ]
    
    for i, issue in enumerate(test_tickets, 1):
        print(f"\n{'─'*70}")
        print(f"📌 TICKET {i}: {issue}")
        print(f"{'─'*70}")
        
        # 1️⃣  AI Reasoning
        print("\n1️⃣  AI CLASSIFICATION")
        decision = process_ticket(issue)
        print(f"   Category: {decision['category']}")
        print(f"   Priority: {decision['priority']}")
        print(f"   Team: {decision['team']}")
        print(f"   Confidence: {decision['confidence']}")
        print(f"   Action: {decision['suggested_action']}")
        
        # 2️⃣  Tool Execution
        print("\n2️⃣  TOOL EXECUTION")
        execution = executor.execute(decision)
        for action in execution["executed"]:
            print(f"   {action}")
        
        # 3️⃣  Memory Store
        print("\n3️⃣  MEMORY STORAGE")
        memory.store_ticket(issue, decision)
        print(f"   ✓ Stored in knowledge base")
        
        # 4️⃣  Show past learning
        print("\n4️⃣  SIMILAR PAST TICKETS (LEARNING)")
        similar = memory.find_similar_tickets(issue)
        if similar:
            for j, sim in enumerate(similar, 1):
                print(f"   {j}. {sim}")
        else:
            print("   (no similar history yet)")
        
        time.sleep(0.5)  # Add slight delay for readability
    
    print(f"\n{'='*70}")
    print("✅ DEMO COMPLETE")
    print(f"{'='*70}")
    
    # Show final memory state
    print(f"\n📊 FINAL MEMORY STATE ({len(memory.tickets)} tickets stored)")
    print(json.dumps(memory.tickets, indent=2))


if __name__ == "__main__":
    demo_flow()
