"""
Execution tools for the autonomous ops agent.
These are mocked for demo purposes but designed to integrate with real systems.
"""

import json
from datetime import datetime
from pathlib import Path

EXECUTION_LOG = Path(__file__).parent / "execution_log.json"


class ExecutionEngine:
    """Execute decisions from the AI agent."""
    
    def __init__(self):
        self.log = []
    
    def log_action(self, action: str, status: str = "success", details: str = ""):
        """Record action execution."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "status": status,
            "details": details
        }
        self.log.append(entry)
        print(f"  ✓ {action}: {details}" if status == "success" else f"  ✗ {action}: {details}")
    
    def send_alert(self, priority: str, issue: str) -> str:
        """Mock Slack/Teams alert."""
        self.log_action(
            "send_alert",
            details=f"Slack alert: [{priority}] {issue[:50]}..."
        )
        return f"Alert sent to #incidents channel"
    
    def assign_ticket(self, team: str, issue: str) -> str:
        """Mock ticket assignment."""
        self.log_action(
            "assign_ticket",
            details=f"Assigned to {team}"
        )
        return f"Ticket assigned to {team}"
    
    def create_jira_ticket(self, category: str, priority: str, summary: str) -> str:
        """Mock Jira ticket creation."""
        ticket_id = f"DEMO-{len(self.log):04d}"
        self.log_action(
            "create_jira_ticket",
            details=f"{ticket_id} [{priority}] {summary[:50]}..."
        )
        return f"Jira ticket {ticket_id} created"
    
    def store_in_knowledge_base(self, issue: str, resolution: str) -> str:
        """Mock knowledge base storage."""
        self.log_action(
            "store_knowledge_base",
            details=f"Stored {len(issue)} chars for future reference"
        )
        return "Stored in knowledge base"
    
    def execute(self, decision: dict) -> dict:
        """Execute all actions from decision."""
        self.log = []  # Reset log for this execution
        
        issue = decision.get("issue", "Unknown issue")
        priority = decision.get("priority", "Medium")
        team = decision.get("team", "General")
        actions = decision.get("suggested_action", "")
        
        executed_actions = []
        
        # Execute based on priority
        if priority == "High" or priority == "Critical":
            executed_actions.append(self.send_alert(priority, issue))
            executed_actions.append(self.create_jira_ticket(
                decision.get("category", "Incident"),
                priority,
                issue
            ))
        
        # Assign to team
        executed_actions.append(self.assign_ticket(team, issue))
        
        # Always store for learning
        executed_actions.append(self.store_in_knowledge_base(issue, actions))
        
        return {
            "executed": executed_actions,
            "action_log": self.log
        }


# Global instance
executor = ExecutionEngine()
