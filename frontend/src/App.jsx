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
          {/* Intro Section */}
          <div
            style={{
              background: "linear-gradient(135deg, #1e3a8a 0%, #1e1b4b 100%)",
              borderRadius: "12px",
              padding: "2rem",
              marginBottom: "2rem",
              border: "1px solid #334155",
            }}
          >
            <h2
              style={{
                margin: "0 0 0.5rem 0",
                fontSize: "1.5rem",
                color: "#e0e7ff",
              }}
            >
              🤖 Welcome to STUAI
            </h2>
            <p
              style={{
                margin: "0 0 1rem 0",
                color: "#93c5fd",
                fontSize: "1rem",
              }}
            >
              <strong>Autonomous Operations Intelligence Platform</strong> -
              Powered by Ollama AI + FastAPI
            </p>
            <p
              style={{
                margin: "0",
                color: "#cbd5e1",
                lineHeight: "1.6",
                maxWidth: "800px",
              }}
            >
              Submit your operational issues and watch our AI instantly classify
              them, assign to the right team, and suggest actions. The system
              learns from your ticket history to improve accuracy over time.{" "}
              <strong>Perfect for automatic ticket routing</strong> and reducing
              mean time to response (MTTR).
            </p>
          </div>

          <div className="grid">
            {/* Left Column: Form & Result */}
            <div>
              <div className="card">
                <h2>🎯 Submit Ticket</h2>
                <TicketForm onTicketSubmitted={handleTicketSubmitted} />
              </div>

              {lastResult && <TicketResult result={lastResult} />}
            </div>

            {/* Right Column: Dashboard */}
            <div>
              <Dashboard allTickets={allTickets} />

              {/* Recent Tickets */}
              <div className="card" style={{ marginTop: "2rem" }}>
                <h2>📋 Recent Tickets</h2>
                <p
                  style={{
                    fontSize: "0.85rem",
                    color: "#6b7280",
                    marginTop: "-0.5rem",
                    marginBottom: "1rem",
                  }}
                >
                  Last {Math.min(5, allTickets.length)} tickets submitted to the
                  system
                </p>
                {allTickets.length === 0 ? (
                  <p
                    style={{
                      color: "#6b7280",
                      marginTop: "1rem",
                      textAlign: "center",
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
