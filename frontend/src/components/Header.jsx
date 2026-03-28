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
        <h1>🤖 STUAI - Autonomous Ops Demo</h1>
        <div className="status">
          <div className={`status-dot ${!isOnline ? "offline" : ""}`} />
          <span>Backend: {isOnline ? "✅ Connected" : "❌ Offline"}</span>
        </div>
      </div>
    </header>
  );
}
