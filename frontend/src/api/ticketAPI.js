import axios from "axios";

const API_BASE = "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
});

export const ticketAPI = {
  // Submit a new ticket for processing
  submitTicket: async (issue, context = "") => {
    try {
      const response = await api.post("/ticket", {
        issue,
        context: context || undefined,
      });
      return response.data;
    } catch (error) {
      throw new Error(
        error.response?.data?.detail || "Failed to submit ticket",
      );
    }
  },

  // Get all stored tickets
  getAllTickets: async () => {
    try {
      const response = await api.get("/memory/tickets");
      return response.data.tickets;
    } catch (error) {
      throw new Error("Failed to fetch tickets");
    }
  },

  // Health check
  healthCheck: async () => {
    try {
      const response = await api.get("/health");
      return response.data.status === "ok";
    } catch (error) {
      return false;
    }
  },
};

export default api;
