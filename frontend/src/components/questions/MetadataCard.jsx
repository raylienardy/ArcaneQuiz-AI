export default function MetadataCard({ title, children }) {
  return (
    <div className="metadata-card">
      <h4 className="metadata-card-title">{title}</h4>
      <div className="metadata-card-body">{children}</div>
    </div>
  );
}
