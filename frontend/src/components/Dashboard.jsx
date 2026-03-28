import { useEffect, useState } from "react";
import { ticketAPI } from "../api/ticketAPI";

export function Dashboard({ allTickets }) {
  const [stats, setStats] = useState({
    total: 0,
    byCategory: {},
    byPriority: {},
  });

  useEffect(() => {
    if (allTickets && allTickets.length > 0) {
      const newStats = {
        total: allTickets.length,
        byCategory: {},
        byPriority: {},
      };

      allTickets.forEach((ticket) => {
        // Count by category (if stored in memory)
        const category = ticket.category || "Unknown";
        newStats.byCategory[category] =
          (newStats.byCategory[category] || 0) + 1;

        // Count by priority (if stored in memory)
        const priority = ticket.priority || "Unknown";
        newStats.byPriority[priority] =
          (newStats.byPriority[priority] || 0) + 1;
      });

      setStats(newStats);
    }
  }, [allTickets]);

  return (
    <div className="card">
      <h2>📊 Dashboard</h2>
      <p style={{ fontSize: "0.85rem", color: "#6b7280", marginTop: "-0.5rem", marginBottom: "1.5rem" }}>
        Real-time operational statistics and ticket classification breakdown
      </p>

      <div className="stats-grid">
        <div className="stat-card" style={{ borderTop: "3px solid #2563eb", background: "linear-gradient(135deg, #f0f9ff 0%, #f3f4f6 100%)" }}>
          <div className="stat-number" style={{ color: "#2563eb" }}>{stats.total}</div>
          <div className="stat-label">Total Tickets</div>
          <div style={{ fontSize: "0.75rem", color: "#6b7280", marginTop: "0.5rem" }}>
            All submitted issues
          </div>
        </div>

        {Object.entries(stats.byCategory).map(([category, count]) => {
          const categoryColors = {
            Incident: "#ef4444",
            Request: "#3b82f6",
            Change: "#f59e0b",
            Problem: "#8b5cf6",
            Unknown: "#6b7280",
          };
          const color = categoryColors[category] || "#6b7280";
          return (
            <div key={category} className="stat-card" style={{ borderTop: `3px solid ${color}`, background: "linear-gradient(135deg, #f3f4f6 0%, #ffffff 100%)" }}>
              <div className="stat-number" style={{ color }}>{count}</div>
              <div className="stat-label">{category}</div>
              <div style={{ fontSize: "0.75rem", color: "#6b7280", marginTop: "0.5rem" }}>
                {category === "Incident" && "Unplanned interruptions"}
                {category === "Request" && "New features/improvements"}
                {category === "Change" && "Planned modifications"}
                {category === "Problem" && "Root cause analysis needed"}
                {category === "Unknown" && "Unclassified"}
              </div>
            </div>
          );
        })}
      </div>

      <h3 style={{ marginTop: "1.5rem", fontSize: "1rem", color: "#1f2937", marginBottom: "0.5rem" }}>⚡ Priority Distribution</h3>
      <p style={{ fontSize: "0.8rem", color: "#6b7280", marginTop: "0 !important", marginBottom: "1rem" }}>
        Breakdown of tickets by urgency and impact level
      </p>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "1rem",
          marginTop: "1rem",
        }}
      >
        {Object.entries(stats.byPriority).map(([priority, count]) => {
          const priorityColors = {
            Critical: { bg: "#fee2e2", text: "#dc2626", border: "#ef4444" },
            High: { bg: "#fef3c7", text: "#d97706", border: "#f59e0b" },
            Medium: { bg: "#dbeafe", text: "#2563eb", border: "#3b82f6" },
            Low: { bg: "#dcfce7", text: "#059669", border: "#10b981" },
            Unknown: { bg: "#f3f4f6", text: "#6b7280", border: "#9ca3af" },
          };
          const colors = priorityColors[priority] || priorityColors.Unknown;
          return (
            <div
              key={priority}
              style={{
                padding: "1rem",
                background: colors.bg,
                borderRadius: "6px",
                fontSize: "0.9rem",
                borderLeft: `3px solid ${colors.border}`,
              }}
            >
              <strong style={{ color: colors.text }}>{priority}</strong>
              <div style={{ fontSize: "1.5rem", fontWeight: "bold", color: colors.text, marginTop: "0.5rem" }}>
                {count}
              </div>
              <div style={{ fontSize: "0.75rem", color: "#6b7280", marginTop: "0.5rem" }}>
                {priority === "Critical" && "System down"}
                {priority === "High" && "Urgent action"}
                {priority === "Medium" && "Should address"}
                {priority === "Low" && "Can wait"}
                {priority === "Unknown" && "Unclassified"}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
