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

const categoryDescriptions = {
  Incident: "Unplanned interruption to service requiring immediate attention",
  Request: "Request for new feature or capability that improves operations",
  Change: "Planned modification to infrastructure or service configuration",
  Problem: "Root cause analysis and resolution assessment needed",
};

const priorityDescriptions = {
  Critical: "Requires immediate action - system unavailable or severely impacted",
  High: "Significant impact - urgent attention recommended within minutes",
  Medium: "Moderate impact - should be addressed within hours",
  Low: "Minor impact - can be scheduled during regular maintenance",
};

const teamDescriptions = {
  DevOps: "Infrastructure, deployment, and operational automation experts",
  Security: "Security incident response and vulnerability management team",
  Database: "Database performance, backup, and recovery specialists",
  Platform: "Platform infrastructure and reliability engineers",
  Frontend: "User interface and client-side application specialists",
  Backend: "Server-side application and API development team",
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
  const confidenceColor = confidence > 85 ? "#10b981" : confidence > 70 ? "#f59e0b" : "#ef4444";

  return (
    <div
      className="ticket-result"
      style={{
        background: "linear-gradient(135deg, #f0f9ff 0%, #f0fdf4 100%)",
        borderLeft: "4px solid #2563eb",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "0.5rem",
          marginBottom: "1.5rem",
        }}
      >
        <span style={{ fontSize: "2rem" }}>✨</span>
        <div>
          <h3 style={{ margin: "0", fontSize: "1.3rem" }}>
            AI Classification Result
          </h3>
          <p
            style={{
              margin: "0.25rem 0 0 0",
              fontSize: "0.85rem",
              color: "#6b7280",
            }}
          >
            Analyzed and classified by Ollama AI in milliseconds
          </p>
        </div>
      </div>

      <div className="classification-grid">
        {/* Category with Description */}
        <div className="classification-item" style={{ borderLeft: "3px solid #ef4444", paddingLeft: "1rem" }}>
          <label style={{ color: "#ef4444", fontWeight: "bold" }}>🏷️ Category</label>
          <value style={{ display: "block", marginTop: "0.5rem" }}>
            <span
              className={`badge ${categoryBadgeClass[classification.category] || "badge-info"}`}
            >
              {classification.category}
            </span>
          </value>
          <small style={{ display: "block", marginTop: "0.5rem", color: "#6b7280", fontSize: "0.8rem" }}>
            {categoryDescriptions[classification.category] || "Operational issue"}
          </small>
        </div>

        {/* Priority with Description */}
        <div className="classification-item" style={{ borderLeft: "3px solid #f59e0b", paddingLeft: "1rem" }}>
          <label style={{ color: "#f59e0b", fontWeight: "bold" }}>⚡ Priority</label>
          <value style={{ display: "block", marginTop: "0.5rem" }}>
            <span
              className={`badge ${priorityBadgeClass[classification.priority] || "badge-info"}`}
            >
              {classification.priority}
            </span>
          </value>
          <small style={{ display: "block", marginTop: "0.5rem", color: "#6b7280", fontSize: "0.8rem" }}>
            {priorityDescriptions[classification.priority] || "Standard response"}
          </small>
        </div>

        {/* Team Assignment with Description */}
        <div className="classification-item" style={{ borderLeft: "3px solid #3b82f6", paddingLeft: "1rem" }}>
          <label style={{ color: "#3b82f6", fontWeight: "bold" }}>👥 Assigned Team</label>
          <value style={{ display: "block", marginTop: "0.5rem", fontWeight: "500" }}>
            {classification.team}
          </value>
          <small style={{ display: "block", marginTop: "0.5rem", color: "#6b7280", fontSize: "0.8rem" }}>
            {teamDescriptions[classification.team] || "Specialist team assigned"}
          </small>
        </div>

        {/* Confidence with Progress Bar */}
        <div className="classification-item" style={{ borderLeft: "3px solid #10b981", paddingLeft: "1rem" }}>
          <label style={{ color: "#10b981", fontWeight: "bold" }}>🧠 AI Confidence</label>
          <value style={{ display: "block", marginTop: "0.5rem" }}>
            <div style={{
              display: "flex",
              alignItems: "center",
              gap: "0.5rem",
            }}>
              <div style={{
                flex: 1,
                height: "8px",
                background: "#e5e7eb",
                borderRadius: "4px",
                overflow: "hidden",
              }}>
                <div style={{
                  height: "100%",
                  width: `${confidence}%`,
                  background: confidenceColor,
                  transition: "all 0.3s ease",
                }} />
              </div>
              <span style={{ fontWeight: "bold", color: confidenceColor, minWidth: "40px" }}>
                {confidence}%
              </span>
            </div>
          </value>
          <small style={{ display: "block", marginTop: "0.5rem", color: "#6b7280", fontSize: "0.8rem" }}>
            {confidence > 85 ? "Highly confident" : confidence > 70 ? "Moderately confident" : "Lower confidence"}
          </small>
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
            borderLeft: "4px solid #3b82f6",
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
          <p style={{ fontSize: "0.85rem", color: "#6b7280", marginTop: "-0.5rem", marginBottom: "1rem" }}>
            The system identified {similar_past_tickets.length} similar issue(s) from your ticket history that could help resolve this issue
          </p>
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
                  cursor: "pointer",
                  transition: "all 0.2s ease",
                }}
                onMouseEnter={(e) => {
                  e.target.style.borderColor = "#3b82f6";
                  e.target.style.boxShadow = "0 2px 4px rgba(59, 130, 246, 0.1)";
                }}
                onMouseLeave={(e) => {
                  e.target.style.borderColor = "#e5e7eb";
                  e.target.style.boxShadow = "none";
                }}
              >
                <strong style={{ color: "#1e40af" }}>#{idx + 1}</strong> {ticket}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Learning Stats Section */}
      <div style={{
        background: "#f3f4f6",
        borderRadius: "6px",
        padding: "1rem",
        marginTop: "1.5rem",
        fontSize: "0.85rem",
        color: "#6b7280",
        borderLeft: "3px solid #8b5cf6",
      }}>
        <p style={{ margin: "0", fontWeight: "500", color: "#7c3aed" }}>
          📚 Learning from History
        </p>
        <p style={{ margin: "0.5rem 0 0 0" }}>
          Your system learns from every ticket submitted. Over time, classification accuracy improves as the AI model 
          sees more diverse operational scenarios and patterns unique to your infrastructure.
        </p>
      </div>
    </div>
  );
}
