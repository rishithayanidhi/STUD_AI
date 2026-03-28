import { useState, useEffect } from "react";
import { Header } from "./components/Header";
import { TicketForm } from "./components/TicketForm";
import { TicketResult } from "./components/TicketResult";
import { Dashboard } from "./components/Dashboard";
import "./index.css";

function App() {
  const [lastResult, setLastResult] = useState(null);
  const [allTickets, setAllTickets] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadAllTickets();
  }, []);

  const loadAllTickets = async () => {
    try {
      setLoading(true);
      const tickets = await (
        await fetch("http://localhost:8000/memory/tickets")
      ).json();
      setAllTickets(tickets.tickets || []);
    } catch (error) {
      console.error("Failed to load tickets:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleTicketSubmitted = (result) => {
    setLastResult(result);
    loadAllTickets();
  };

  return (
    <>
      <Header />
      <main style={{ flex: 1 }}>
        <div className="container">
          {/* Main Grid Layout */}
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: "1.5rem",
              marginTop: "2rem",
            }}
          >
            {/* Top Left: Submit Ticket Form */}
            <div className="card">
              <h2 style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                <span>📝</span> Submit Ticket
              </h2>
              <p style={{ fontSize: "0.8rem", color: "#94a3b8", marginTop: "-0.5rem", marginBottom: "1rem" }}>
                Describe your operational issue
              </p>
              <TicketForm onTicketSubmitted={handleTicketSubmitted} />
            </div>

            {/* Top Right: Submit Overview */}
            <div className="card">
              <h2 style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                <span>📊</span> Submit Overview
              </h2>
              <p style={{ fontSize: "0.8rem", color: "#94a3b8", marginTop: "-0.5rem", marginBottom: "1rem" }}>
                System statistics and metrics
              </p>
              <Dashboard allTickets={allTickets} />
            </div>

            {/* Bottom Left: PostgreSQL Checkpoint */}
            <div className="card">
              <h2 style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                <span>🗄️</span> PostgreSQL Checkpoint
              </h2>
              <p style={{ fontSize: "0.8rem", color: "#94a3b8", marginTop: "-0.5rem", marginBottom: "1rem" }}>
                Database connection and status
              </p>
              <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                <div style={{ padding: "0.75rem", background: "#0f172a", borderRadius: "6px", border: "1px solid #334155" }}>
                  <span style={{ fontSize: "0.85rem", color: "#94a3b8" }}>Total Records</span>
                  <div style={{ fontSize: "1.5rem", fontWeight: "bold", color: "#60a5fa", marginTop: "0.25rem" }}>
                    {allTickets.length}
                  </div>
                </div>
                <div style={{ padding: "0.75rem", background: "#0f172a", borderRadius: "6px", border: "1px solid #334155" }}>
                  <span style={{ fontSize: "0.85rem", color: "#94a3b8" }}>Status</span>
                  <div style={{ fontSize: "0.9rem", color: "#10b981", marginTop: "0.25rem" }}>
                    ✅ Connected
                  </div>
                </div>
              </div>
            </div>

            {/* Bottom Right: Classification Result */}
            <div>
              {lastResult ? (
                <TicketResult result={lastResult} />
              ) : (
                <div className="card">
                  <h2 style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                    <span>⚙️</span> AI Classification
                  </h2>
                  <p style={{ fontSize: "0.8rem", color: "#94a3b8", marginTop: "-0.5rem", marginBottom: "1rem" }}>
                    Submit a ticket to see AI analysis
                  </p>
                  <div style={{ textAlign: "center", padding: "2rem", color: "#64748b" }}>
                    <div style={{ fontSize: "2.5rem", marginBottom: "0.5rem" }}>🔄</div>
                    <p>Awaiting ticket submission...</p>
                  </div>
                </div>
              )}
            </div>

            {/* Recent Tickets (Full Width) */}
            <div className="card" style={{ gridColumn: "1 / -1" }}>
              <h2 style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                <span>📋</span> Recent Tickets
              </h2>
              <p style={{ fontSize: "0.8rem", color: "#94a3b8", marginTop: "-0.5rem", marginBottom: "1rem" }}>
                Last {Math.min(10, allTickets.length)} tickets from the system
              </p>
              {allTickets.length === 0 ? (
                <p style={{ color: "#64748b", textAlign: "center", padding: "2rem" }}>
                  No tickets yet. Submit one to get started!
                </p>
              ) : (
                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))",
                    gap: "1rem",
                  }}
                >
                  {[...allTickets].reverse().slice(0, 10).map((ticket, idx) => (
                    <div
                      key={idx}
                      style={{
                        padding: "1rem",
                        background: "#0f172a",
                        border: "1px solid #334155",
                        borderRadius: "6px",
                        cursor: "pointer",
                        transition: "all 0.2s ease",
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.borderColor = "#3b82f6";
                        e.currentTarget.style.boxShadow = "0 2px 8px rgba(59, 130, 246, 0.2)";
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.borderColor = "#334155";
                        e.currentTarget.style.boxShadow = "none";
                      }}
                    >
                      <div style={{ fontSize: "0.8rem", color: "#94a3b8", marginBottom: "0.5rem" }}>
                        Ticket #{idx + 1}
                      </div>
                      <div style={{ fontSize: "0.85rem", color: "#cbd5e1", lineHeight: "1.4" }}>
                        {typeof ticket === "string" ? ticket : ticket.issue || JSON.stringify(ticket).substring(0, 60)}
                      </div>
                      {typeof ticket !== "string" && ticket.category && (
                        <div style={{ marginTop: "0.75rem", display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
                          <span className="badge badge-info">{ticket.category}</span>
                          <span className="badge badge-warning">{ticket.priority}</span>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </>
  );
                      padding: "2rem",
                    }}
                  >
                    <span
                      style={{
                        fontSize: "2rem",
                        display: "block",
                        marginBottom: "0.5rem",
                      }}
                    >
                      📭
                    </span>
                    No tickets yet. Submit one to get started!
                  </p>
                ) : (
                  <div className="ticket-list">
                    {[...allTickets]
                      .reverse()
                      .slice(0, 5)
                      .map((ticket, idx) => (
                        <div key={idx} className="ticket-item">
                          <div className="ticket-item-header">
                            <div className="ticket-item-title">
                              {typeof ticket === "string"
                                ? ticket
                                : ticket.issue ||
                                  JSON.stringify(ticket).substring(0, 50)}
                            </div>
                          </div>
                          {typeof ticket !== "string" && ticket.category && (
                            <div className="ticket-item-meta">
                              <span className="badge badge-info">
                                {ticket.category}
                              </span>
                              <span className="badge badge-warning">
                                {ticket.priority}
                              </span>
                            </div>
                          )}
                        </div>
                      ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>

      <footer>
        <p>
          🚀 STUAI - Autonomous Operations Demo | Powered by Ollama + FastAPI
        </p>
      </footer>
    </>
  );
}

export default App;
