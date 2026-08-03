import api from "./api";

export async function generateQuestions(payload, debug = false) {
  const params = debug ? { debug: true } : {};
  const response = await api.post("/questions/generate", payload, { params });
  return response.data;
}
