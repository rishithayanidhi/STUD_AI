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

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-number">{stats.total}</div>
          <div className="stat-label">Total Tickets</div>
        </div>

        {Object.entries(stats.byCategory).map(([category, count]) => (
          <div key={category} className="stat-card">
            <div className="stat-number">{count}</div>
            <div className="stat-label">{category}</div>
          </div>
        ))}
      </div>

      <h3 style={{ marginTop: "1.5rem", fontSize: "1rem" }}>By Priority</h3>
      <div
        style={{
          display: "flex",
          gap: "1rem",
          marginTop: "1rem",
          flexWrap: "wrap",
        }}
      >
        {Object.entries(stats.byPriority).map(([priority, count]) => (
          <div
            key={priority}
            style={{
              padding: "0.75rem 1rem",
              background: "#f3f4f6",
              borderRadius: "6px",
              fontSize: "0.9rem",
            }}
          >
            <strong>{priority}:</strong> {count}
          </div>
        ))}
      </div>
    </div>
  );
}
