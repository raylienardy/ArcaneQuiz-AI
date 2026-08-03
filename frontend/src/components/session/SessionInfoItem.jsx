export default function SessionInfoItem({ label, value }) {
  return (
    <div className="session-info-item">
      <span className="session-label">{label}</span>
      <span className="session-value">{value ?? "—"}</span>
    </div>
  );
}
