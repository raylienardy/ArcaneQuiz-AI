import api from "./api";

/**
 * Check backend health status.
 * @returns {Promise<{status: string, message: string}>}
 */
export async function checkHealth() {
  const response = await api.get("/health");
  return response.data;
}
