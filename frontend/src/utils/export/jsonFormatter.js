export function formatJSON(questions, metadata = {}) {
  const output = {
    metadata,
    questions,
  };
  return JSON.stringify(output, null, 2);
}
