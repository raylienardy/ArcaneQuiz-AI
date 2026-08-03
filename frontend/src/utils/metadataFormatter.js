export function formatLatency(seconds) {
  if (seconds == null) return "—";
  if (seconds < 1) return `${Math.round(seconds * 1000)} ms`;
  return `${seconds.toFixed(2)} s`;
}

export function formatTimestamp(isoString) {
  if (!isoString) return "—";
  return new Date(isoString).toLocaleString();
}
