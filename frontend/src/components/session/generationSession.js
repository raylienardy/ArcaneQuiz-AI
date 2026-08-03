/**
 * Fungsi-fungsi murni untuk membuat objek sesi generasi.
 */

export function createSession({
  provider,
  model,
  generationTime,
  questionCount,
  language,
  difficulty,
  questionType,
  promptVersion,
  schemaVersion,
  status,
}) {
  return {
    generatedAt: new Date().toISOString(),
    provider: provider || "unknown",
    model: model || "unknown",
    generationTime: generationTime ?? null,
    questionCount: questionCount ?? 0,
    language: language || "unknown",
    difficulty: difficulty || "unknown",
    questionType: questionType || "unknown",
    promptVersion: promptVersion || "—",
    schemaVersion: schemaVersion || "—",
    status: status || "completed",
  };
}

export function clearSession() {
  return null;
}

export function updateSession(prevSession, updates) {
  return { ...prevSession, ...updates };
}
