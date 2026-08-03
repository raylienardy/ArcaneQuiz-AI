/**
 * Daftar pesan loading untuk berbagai tahapan.
 */
export const LOADING_MESSAGES = {
  upload: "Uploading file...",
  extraction: "Extracting document...",
  connecting: "Connecting to AI provider...",
  generating: "Generating questions...",
  parsing: "Parsing response...",
  validating: "Validating questions...",
  default: "Please wait...",
};

export function getLoadingMessage(stage = "default") {
  return LOADING_MESSAGES[stage] || LOADING_MESSAGES.default;
}
