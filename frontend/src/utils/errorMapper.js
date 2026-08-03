/**
 * Konversi error API menjadi pesan ramah pengguna.
 * @param {Error|object} error - Objek error dari Axios atau string.
 * @returns {object} { title, description, retry: boolean }
 */
export function mapApiError(error) {
  if (!error)
    return {
      title: "Unknown Error",
      description: "Something went wrong.",
      retry: true,
    };

  // Jika error berasal dari Axios dengan response
  const status = error.response?.status;
  const detail = error.response?.data?.detail || "";

  if (status === 401)
    return {
      title: "Authentication Error",
      description: detail || "Invalid API key.",
      retry: false,
    };
  if (status === 429)
    return {
      title: "Too Many Requests",
      description: detail || "Rate limit exceeded.",
      retry: true,
    };
  if (status === 413)
    return {
      title: "File Too Large",
      description: detail || "Maximum size is 20MB.",
      retry: false,
    };
  if (status === 415)
    return {
      title: "Unsupported File",
      description: detail || "Only PDF, DOCX, TXT are allowed.",
      retry: false,
    };
  if (status === 422)
    return {
      title: "Validation Error",
      description: detail || "The request was invalid.",
      retry: false,
    };
  if (status === 502)
    return {
      title: "AI Provider Error",
      description:
        "Unable to communicate with the AI provider. Please try again later.",
      retry: true,
    };
  if (status === 504)
    return {
      title: "Timeout",
      description: "The AI took too long to respond. Please try again.",
      retry: true,
    };
  if (error.request && !error.response)
    return {
      title: "Network Error",
      description:
        "Unable to connect to the server. Check your internet connection.",
      retry: true,
    };

  // Fallback
  return {
    title: "Error",
    description: detail || error.message || "Something went wrong.",
    retry: true,
  };
}
