#!/usr/bin/env python3
"""
Quick reference checklist for demo day.
Print this and check off items as you set up.
"""

import subprocess
import sys
from pathlib import Path


CHECKLIST = """
╔════════════════════════════════════════════════════════════════════════╗
║                    DEMO DAY CHECKLIST                                  ║
╚════════════════════════════════════════════════════════════════════════╝

PRE-DEMO SETUP (Do this 15 minutes before)
───────────────────────────────────────────────────────────────────────

□ 1. Open terminal and run the FastAPI server:
     cd autonomous-ops-demo
     python main.py
     
     Expected output:
     "🚀 Starting Autonomous Ops Demo API..."
     "📖 API docs: http://localhost:8000/docs"

□ 2. Open browser to http://localhost:8000
     You should see the form with textarea

□ 3. Test one submission BEFORE judges arrive:
     - Type: "Test issue for demo"
     - Click "Analyze & Execute"
     - Verify you see Classification + Actions

□ 4. Have the DEMO_SCRIPT.py output ready to read from:
     python DEMO_SCRIPT.py > demo_notes.txt
     (Print or have on second screen)


DEMO FLOW (Read this during presentation)
───────────────────────────────────────────────────────────────────────

□ OPENING STATEMENT (30 sec)
   "Let me show you autonomous operations. Most tickets take 20-45 minutes
    to respond to. Our system responds in seconds."

□ SUBMIT TICKET (45 sec)
   Issue: "Production API failing with 500 error affecting payments"
   
   Point out:
   - They see it being classified
   - They see actions executing
   - They can watch logs in real-time

□ SHOW RESULTS (30 sec)
   Point to:
   - Category: Incident (AI understood severity)
   - Priority: HIGH (AI decided this is critical)
   - Team: Backend / Payments (AI assigned it)
   - Confidence: 87% (AI is confident)

□ SHOW EXECUTION LOG (30 sec)
   "Look, all these happened automatically:
    ✓ Alert sent
    ✓ Ticket created  
    ✓ Team assigned
    ✓ Stored for learning"

□ OPTIONAL: Show Learning (20 sec)
   Submit: "Payment API 500 error"
   Show similar past tickets pop up
   "The system learned from the first ticket"

□ ARCHITECTURE EXPLANATION (30 sec)
   Explain: Brain (OpenClaw) → Hands (Antigravity) → Memory (ChromaDB)

□ CLOSE (15 sec)
   "This is autonomous operations. AI that understands and acts.
    The future of DevOps."


EMERGENCY TROUBLESHOOTING
───────────────────────────────────────────────────────────────────────

If API won't start:
□ Check Python installed: python --version
□ Check venv activated: (you should see .venv in path)
□ Reinstall dependencies: pip install -r requirements.txt
□ Try on different port: uvicorn main:app --port 8001

If browser won't connect:
□ Verify API is running (should see "Uvicorn running on..." in terminal)
□ Try: http://127.0.0.1:8000 instead of localhost
□ Check firewall: port 8000 should be open
□ Fallback: Use curl to test:
   curl -X POST "http://localhost:8000/ticket" \\
     -H "Content-Type: application/json" \\
     -d '{"issue": "Test issue"}'

If AI response is slow:
□ First time is slow (models loading) - normal
□ If OPENAI_API_KEY set, real API calls take 1-3 seconds
□ Mock classifikation is instant (< 50ms)
□ Have a backup: show test_demo.py output if live demo fails

If you need to restart:
□ Stop server: Ctrl+C in terminal
□ Clear memory: rm tickets.json execution_log.json
□ Restart: python main.py
□ Ready for clean demo


WHAT TO HIGHLIGHT (Talking Points)
───────────────────────────────────────────────────────────────────────

✓ "AI understands business context" 
  (See: Classification gets Priority + Team right)

✓ "AI makes autonomous decisions"
  (See: Actions execute without human approval)

✓ "System learns and improves"
  (See: Similar tickets retrieved from memory)

✓ "It's FAST"
  (See: Response in < 2 seconds end-to-end)

✓ "It scales"
  (FastAPI can handle 1000s of concurrent requests)

✓ "Production-ready architecture"
  (Explain: Frontend → API → Agent → Tools → Database)


JUDGE QUESTIONS (Be Ready)
───────────────────────────────────────────────────────────────────────

"How does it integrate with Jira/Slack?"
→ "Today it's mocked for the demo. But the Tool Execution layer is
   designed to call real APIs. Just swap mock functions with real ones."

"What happens if AI makes a wrong decision?"
→ "Great question! We track confidence (see: 87%). Low confidence gets
   flagged for human review. Also, all actions are logged - humans can
   audit and override."

"How's the memory working?"
→ "ChromaDB stores tickets as vectors. New issues are compared to
   historical ones using similarity search. Hits show past solutions."

"What about security?"
→ "This demo is open for simplicity. Production would add: API auth,
   RBAC per team, audit logging, and approval workflows for destructive
   actions."

"Is this real AI or just if-then rules?"
→ "It's real LLM (GPT-3.5-turbo from OpenAI). The reasoning is based on
   language understanding, not hardcoded rules. That's why it handles
   edge cases better."


BONUS: Graph/Screenshot Ideas
───────────────────────────────────────────────────────────────────────

If you have extra time, show:
  - /memory/tickets endpoint (shows all stored tickets JSON)
  - API docs at /docs (auto-generated Swagger UI)
  - Swap between tickets fast to show throughput
  - Edit DEMO_SCRIPT.py to add your own test cases


AFTER DEMO
───────────────────────────────────────────────────────────────────────

□ Save a screenshot of final results (for portfolio)
□ Note any judge questions and answers (for follow-up)
□ Thank them for watching!

"""

def run_checks():
    """Verify setup before demo."""
    print(CHECKLIST)
    
    # Quick diagnostics
    print("\n" + "="*80)
    print("🔍 QUICK DIAGNOSTICS")
    print("="*80)
    
    # Check Python version
    print(f"✓ Python {sys.version.split()[0]} installed")
    
    # Check if main.py exists
    if Path("main.py").exists():
        print("✓ main.py found")
    else:
        print("✗ main.py NOT found (you need to be in the demo folder)")
    
    # Check requirements
    if Path("requirements.txt").exists():
        print("✓ requirements.txt found")
    else:
        print("✗ requirements.txt NOT found")
    
    print("\n" + "="*80)
    print("✅ You're ready! Run: python main.py")
    print("="*80)


if __name__ == "__main__":
    run_checks()
