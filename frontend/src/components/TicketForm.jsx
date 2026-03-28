import { useState } from "react";
import { ticketAPI } from "../api/ticketAPI";

export function TicketForm({ onTicketSubmitted }) {
  const [issue, setIssue] = useState("");
  const [context, setContext] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!issue.trim()) {
      setError("Please enter an issue description");
      return;
    }

    setLoading(true);
    try {
      const result = await ticketAPI.submitTicket(issue, context);
      setIssue("");
      setContext("");
      onTicketSubmitted(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div
        style={{
          background: "#1e3a8a",
          border: "1px solid #3b82f6",
          borderRadius: "8px",
          padding: "1rem",
          marginBottom: "1.5rem",
        }}
      >
        <p style={{ fontSize: "0.9rem", color: "#93c5fd", margin: "0" }}>
          <strong>💡 How it works:</strong> Describe your operational issue and
          our AI will instantly classify it, assign it to the right team, and
          suggest an action.
        </p>
      </div>

      <div className="form-group">
        <label htmlFor="issue">
          <span
            style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}
          >
            🎯 Incident Description <span style={{ color: "#dc2626" }}>*</span>
          </span>
        </label>
        <p
          style={{
            fontSize: "0.85rem",
            color: "#94a3b8",
            marginTop: "-0.5rem",
            marginBottom: "0.5rem",
          }}
        >
          Be clear and specific about the issue. Include error codes, affected
          services, and impact if possible.
        </p>
        <textarea
          id="issue"
          value={issue}
          onChange={(e) => setIssue(e.target.value)}
          placeholder="Example: Database connection timeout in production - Unable to connect to primary database. Error: connection refused on port 5432. Affecting 50+ customers."
          disabled={loading}
          style={{ minHeight: "120px" }}
        />
        <small
          style={{ color: "#64748b", display: "block", marginTop: "0.25rem" }}
        >
          {issue.length} characters
        </small>
      </div>

      <div className="form-group">
        <label htmlFor="context">
          <span
            style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}
          >
            📝 Additional Context (Optional)
          </span>
        </label>
        <p
          style={{
            fontSize: "0.85rem",
            color: "#94a3b8",
            marginTop: "-0.5rem",
            marginBottom: "0.5rem",
          }}
        >
          Add environment details, recent changes, or steps to reproduce.
        </p>
        <textarea
          id="context"
          value={context}
          onChange={(e) => setContext(e.target.value)}
          placeholder="e.g., Environment: Production | Version: 2.4.1 | Started: 2 hours ago | Related tickets: #1234, #1235"
          style={{ minHeight: "80px" }}
          disabled={loading}
        />
      </div>

      {error && (
        <div
          className="alert alert-danger"
          style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}
        >
          <span>⚠️</span> {error}
        </div>
      )}

      <button
        type="submit"
        className="btn-primary"
        disabled={loading}
        style={{ width: "100%", fontSize: "1rem", padding: "1rem" }}
      >
        {loading ? (
          <>
            <span className="loading" />
            🤖 AI is analyzing your ticket...
          </>
        ) : (
          "🚀 Submit for AI Classification"
        )}
      </button>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "1rem",
          marginTop: "1.5rem",
        }}
      >
        <div
          style={{
            padding: "1rem",
            background: "#1e3a8a",
            borderRadius: "6px",
            fontSize: "0.85rem",
            color: "#fbbf24",
            border: "1px solid #3b82f6",
          }}
        >
          <strong>⚡ Speed:</strong> Classification in 2-3 seconds
        </div>
        <div
          style={{
            padding: "1rem",
            background: "#1e293b",
            borderRadius: "6px",
            fontSize: "0.85rem",
            color: "#60a5fa",
            border: "1px solid #334155",
          }}
        >
          <strong>🧠 Accuracy:</strong> Learns from your tickets
        </div>
      </div>
    </form>
  );
}
