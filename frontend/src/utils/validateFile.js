const ALLOWED_EXTENSIONS = ["pdf", "docx", "txt"];
const MAX_SIZE = 20 * 1024 * 1024; // 20 MB

/**
 * Validate a file against allowed types and maximum size.
 * @param {File} file
 * @returns {string|null} error message or null if valid
 */
export function validateFile(file) {
  if (!file) {
    return "No file selected.";
  }

  const extension = file.name.split(".").pop().toLowerCase();
  if (!ALLOWED_EXTENSIONS.includes(extension)) {
    return `Unsupported file type (.${extension}). Please upload PDF, DOCX, or TXT files.`;
  }

  if (file.size > MAX_SIZE) {
    const sizeMB = (file.size / (1024 * 1024)).toFixed(1);
    return `File size (${sizeMB} MB) exceeds the maximum allowed size (20 MB).`;
  }

  return null; // valid
}
