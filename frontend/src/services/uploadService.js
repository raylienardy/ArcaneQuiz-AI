import api from "./api";

/**
 * Upload a file to the backend.
 * @param {File} file
 * @returns {Promise<object>} response data
 */
export async function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post("/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return response.data;
}
