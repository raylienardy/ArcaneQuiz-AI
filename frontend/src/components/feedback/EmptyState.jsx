export default function EmptyState({ title, description, action }) {
  return (
    <div className="empty-state">
      <div className="empty-icon">📭</div>
      <h3>{title || "No data"}</h3>
      <p>{description || "There is nothing to display."}</p>
      {action && (
        <button onClick={action.onClick}>{action.label || "Action"}</button>
      )}
    </div>
  );
}
