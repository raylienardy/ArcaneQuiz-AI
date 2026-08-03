import { useState, useEffect } from "react";
import { checkHealth } from "../services/healthService";

export function useHealthCheck() {
  const [state, setState] = useState({
    isLoading: true,
    isConnected: false,
    status: "",
    message: "",
    error: null,
  });

  useEffect(() => {
    let cancelled = false;

    async function fetchHealth() {
      try {
        const data = await checkHealth();
        if (!cancelled) {
          setState({
            isLoading: false,
            isConnected: true,
            status: data.status,
            message: data.message,
            error: null,
          });
        }
      } catch (err) {
        if (!cancelled) {
          setState({
            isLoading: false,
            isConnected: false,
            status: "",
            message: "",
            error: err.message || "Connection failed",
          });
        }
      }
    }

    fetchHealth();

    return () => {
      cancelled = true;
    };
  }, []);

  return state;
}
