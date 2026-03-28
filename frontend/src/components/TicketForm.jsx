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
      <div className="form-group">
        <label htmlFor="issue">Issue Description *</label>
        <textarea
          id="issue"
          value={issue}
          onChange={(e) => setIssue(e.target.value)}
          placeholder="e.g., Database connection timeout in production..."
          disabled={loading}
        />
      </div>

      <div className="form-group">
        <label htmlFor="context">Additional Context (Optional)</label>
        <textarea
          id="context"
          value={context}
          onChange={(e) => setContext(e.target.value)}
          placeholder="Add any additional information..."
          style={{ minHeight: "80px" }}
          disabled={loading}
        />
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      <button type="submit" className="btn-primary" disabled={loading}>
        {loading ? (
          <>
            <span className="loading" />
            Processing...
          </>
        ) : (
          "🚀 Submit Ticket"
        )}
      </button>
    </form>
  );
}
