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
                {allTickets.length === 0 ? (
                  <p style={{ color: "#6b7280", marginTop: "1rem" }}>
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
