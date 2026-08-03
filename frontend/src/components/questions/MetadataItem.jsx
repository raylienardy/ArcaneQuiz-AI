export default function MetadataItem({ label, value }) {
  return (
    <div className="metadata-item">
      <span className="metadata-label">{label}</span>
      <span className="metadata-value">{value ?? "—"}</span>
    </div>
  );
}
