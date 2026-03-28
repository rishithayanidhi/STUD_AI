import { useEffect, useState } from "react";
import { ticketAPI } from "../api/ticketAPI";

export function Header() {
  const [isOnline, setIsOnline] = useState(false);

  useEffect(() => {
    const checkHealth = async () => {
      const online = await ticketAPI.healthCheck();
      setIsOnline(online);
    };

    checkHealth();
    const interval = setInterval(checkHealth, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header>
      <div className="container">
        <div style={{ textAlign: "center", paddingBottom: "1rem" }}>
          <div
            style={{
              fontSize: "0.9rem",
              color: "#93c5fd",
              marginBottom: "0.5rem",
              letterSpacing: "1px",
            }}
          >
            🤖 AI Powered Automation
          </div>
          <h1
            style={{
              fontSize: "2.5rem",
              fontWeight: "bold",
              margin: "0 0 0.25rem 0",
              color: "#ffffff",
            }}
          >
            Operations Copilot
          </h1>
          <p
            style={{
              fontSize: "0.85rem",
              color: "#cbd5e1",
              margin: "0",
              letterSpacing: "0.5px",
            }}
          >
            AI Powered Incident Automation & Autonomous Decision Making
          </p>
        </div>
        <div
          className="status"
          style={{ justifyContent: "center", gap: "1rem" }}
        >
          <div className={`status-dot ${!isOnline ? "offline" : ""}`} />
          <span style={{ fontSize: "0.9rem" }}>
            Backend: {isOnline ? "✅ Connected" : "❌ Offline"}
          </span>
        </div>
      </div>
    </header>
  );
}
