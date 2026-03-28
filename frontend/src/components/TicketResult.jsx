import React from "react";

const priorityBadgeClass = {
  Critical: "badge-danger",
  High: "badge-warning",
  Medium: "badge-info",
  Low: "badge-success",
};

const categoryBadgeClass = {
  Incident: "badge-danger",
  Request: "badge-info",
  Change: "badge-warning",
  Problem: "badge-danger",
};

export function TicketResult({ result }) {
  if (!result) return null;

  const {
    classification,
    actions_executed,
    execution_log,
    similar_past_tickets,
  } = result;
  const confidence = Math.round((classification.confidence || 0) * 100);

  return (
    <div className="ticket-result">
      <h3>✨ AI Classification Result</h3>

      <div className="classification-grid">
        <div className="classification-item">
          <label>Category</label>
          <value>
            <span
              className={`badge ${categoryBadgeClass[classification.category] || "badge-info"}`}
            >
              {classification.category}
            </span>
          </value>
        </div>

        <div className="classification-item">
          <label>Priority</label>
          <value>
            <span
              className={`badge ${priorityBadgeClass[classification.priority] || "badge-info"}`}
            >
              {classification.priority}
            </span>
          </value>
        </div>

        <div className="classification-item">
          <label>Team</label>
          <value>{classification.team}</value>
        </div>

        <div className="classification-item">
          <label>Confidence</label>
          <value>{confidence}%</value>
        </div>
      </div>

      <div className="action-section">
        <h4>📋 Suggested Action</h4>
        <p
          style={{
            padding: "1rem",
            background: "#f0f9ff",
            borderRadius: "6px",
            color: "#1e40af",
          }}
        >
          {classification.suggested_action}
        </p>
      </div>

      {actions_executed && actions_executed.length > 0 && (
        <div className="action-section">
          <h4>⚙️ Actions Executed ({actions_executed.length})</h4>
          <div className="action-log">
            {actions_executed.map((action, idx) => (
              <div key={idx} className="action-log-item">
                ✓ {action}
              </div>
            ))}
          </div>
        </div>
      )}

      {execution_log && execution_log.length > 0 && (
        <div className="action-section">
          <h4>📝 Execution Log</h4>
          <div className="action-log">
            {execution_log.map((log, idx) => (
              <div key={idx} className="action-log-item">
                {log}
              </div>
            ))}
          </div>
        </div>
      )}

      {similar_past_tickets && similar_past_tickets.length > 0 && (
        <div className="action-section">
          <h4>🔗 Similar Past Tickets</h4>
          <div
            style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}
          >
            {similar_past_tickets.map((ticket, idx) => (
              <div
                key={idx}
                style={{
                  padding: "0.75rem",
                  background: "white",
                  border: "1px solid #e5e7eb",
                  borderRadius: "6px",
                  fontSize: "0.85rem",
                }}
              >
                {ticket}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
