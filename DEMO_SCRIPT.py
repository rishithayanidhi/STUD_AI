"""
DEMO SCRIPT FOR JUDGES - Read this during presentation
Follow this script to deliver a compelling 3-minute autonomous ops demo

🎯 OBJECTIVE: Prove that AI can understand, decide, and execute automatically
"""

DEMO_SCRIPT = """
╔════════════════════════════════════════════════════════════════════════╗
║                    AUTONOMOUS OPS DEMO - JUDGE SCRIPT                  ║
║                              ~3 minutes                                 ║
╚════════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════
OPENING (30 seconds)
═══════════════════════════════════════════════════════════════════════════

"Welcome to the Autonomous Ops Demo. 

In most companies, IT problems flow like this:
    Issue → Human reads it → Human decides → Human acts
    
This takes time. Critical issues wait for humans to wake up.

Our system does this:
    Issue → AI reads it → AI decides → Tools act autonomously
    
Let me show you how it works in real-time."


═══════════════════════════════════════════════════════════════════════════
DEMO STAGE 1: Submit a Ticket (45 seconds)
═══════════════════════════════════════════════════════════════════════════

[Open browser to http://localhost:8000 (or show Postman)]

"Here's our demo. I'm going to submit a critical production issue:

    'Production API failing with 500 error affecting payments'"

[Type/paste the issue into the form and click Submit]

"Notice three things are about to happen:
    1. AI understands the ticket
    2. System makes an autonomous decision
    3. Actions execute automatically"


═══════════════════════════════════════════════════════════════════════════
DEMO STAGE 2: Show AI Reasoning (30 seconds)
═══════════════════════════════════════════════════════════════════════════

[Wait for result, then point to the output]

"Look at what the AI decided:

    Category: Incident
    Priority: HIGH ⬅️  This is key - it's HIGH, not medium
    Assigned to: Backend / Payments Team
    Confidence: 87% ⬅️  The system is confident in this decision"

"The AI didn't just classify it. It made a DECISION about severity and ownership."


═══════════════════════════════════════════════════════════════════════════
DEMO STAGE 3: Show Tool Execution (30 seconds)
═══════════════════════════════════════════════════════════════════════════

"Based on that decision, watch what happened automatically:

    ✓ Alert sent: HIGH PRIORITY payment incident
    ✓ Jira ticket DEMO-0001 created
    ✓ Assigned to Backend / Payments
    ✓ Stored in knowledge base"

"All of this happened without a human operator. The system SAW the severity
and ACTED on it. That's autonomous operations."


═══════════════════════════════════════════════════════════════════════════
DEMO STAGE 4: Show Learning (20 seconds) [OPTIONAL - IF TIME]
═══════════════════════════════════════════════════════════════════════════

"Now the system has learned. Try a similar issue:

    'Payment API returning 500 errors'"

[Submit the new ticket]

"Watch what happens. The system says:

    Similar past tickets found:
    • 'Production API failing with 500 error affecting payments'"

"It's not just solving problems. It's LEARNING from them.

Tomorrow, when a similar issue hits at 3 AM, the system already knows
what the Backend team did to fix it."


═══════════════════════════════════════════════════════════════════════════
CLOSING: The Architecture (30 seconds)
═══════════════════════════════════════════════════════════════════════════

"Here's the architecture that makes this work:

    Frontend (the form you see)
        ↓
    FastAPI (listens for tickets)
        ↓
    OpenClaw Agent (AI reasoning - understands severity, ownership)
        ↓
    Tool Execution Layer (Antigravity integrations - sends alerts, creates tickets)
        ↓
    Vector Memory (ChromaDB - stores what we learned)
        ↓
    Returns decision to user

Think of it as:
    OpenClaw = Brain (decides what to do)
    Antigravity = Hands (does the actions)
    ChromaDB = Memory (learns from experience)
    FastAPI = Nervous system (connects everything)

This proves three essential things about autonomous operations:

    ✓ AI CAN understand complex business context
    ✓ AI CAN make decisions without human intervention
    ✓ AI CAN execute real actions and learn from them


═══════════════════════════════════════════════════════════════════════════
WHY THIS MATTERS (15 seconds)
═══════════════════════════════════════════════════════════════════════════

"Typical incident response:
    • Takes 5-10 minutes just to detect
    • Takes 10-20 minutes for human to classify
    • Takes 5-15 minutes to execute fix
    = 20-45 minute MTTR (Mean Time To Recovery)

Our system:
    • Detects and classifies instantly
    • Executes in seconds
    • Learns from every incident
    = Potential for sub-minute MTTR


═══════════════════════════════════════════════════════════════════════════
QUESTIONS JUDGES MIGHT ASK
═══════════════════════════════════════════════════════════════════════════

Q: "How does this scale? What if you get 1000 tickets?"
A: "The FastAPI backend scales horizontally. Each ticket takes <100ms to
   classify and <50ms to execute. At 1000 tickets/minute, you'd need maybe
   5-10 API instances running in parallel. The async architecture handles it."

Q: "What about false positives? What if the AI classifies wrong?"
A: "Good question. We track accuracy metrics. Initial confidence threshold
   is 0.75 (75%). For anything below that, it flags for human review.
   High-confidence decisions go straight through."

Q: "Can it handle edge cases?"
A: "We built it with OpenAI GPT-3.5 (can upgrade to GPT-4). It handles
   context well, but yes—if something is completely outside training domain,
   it marks it for human. That's actually a safety feature."

Q: "Integration with existing tools?"
A: "Today, we're using mock integrations to prove the concept. But the
   Tool Execution layer (Antigravity) is designed to plug into:
   - Jira APIs
   - Slack webhooks
   - PagerDuty
   - Custom runbooks
   
   Any tool with an API can be a 'skill' the AI learns to use."

Q: "What about security?"
A: "Right now it's a demo, so no authentication. In production, you'd add:
   - API key validation
   - RBAC (role-based access control)
   - Audit logging on every decision+action
   - Human-in-the-loop approval for destructive actions
   
   The AI would only execute actions it's been explicitly granted permission for."


═══════════════════════════════════════════════════════════════════════════
PARTING THOUGHT
═══════════════════════════════════════════════════════════════════════════

"Most of DevOps today is manual or simple rule-based. The future is 
AI that actually _understands_ your systems and _acts_ on that understanding.

This demo shows that future is possible _today_."

"""

if __name__ == "__main__":
    print(DEMO_SCRIPT)
    print("\n" + "="*80)
    print("💡 TIP: Print this script. Practice delivering it in 3 minutes.")
    print("    Timing is everything. Keep it punchy.")
    print("="*80)
