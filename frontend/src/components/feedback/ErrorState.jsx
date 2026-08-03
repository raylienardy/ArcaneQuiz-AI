export default function ErrorState({ title, description, onRetry }) {
  return (
    <div className="error-state">
      <div className="error-icon">❌</div>
      <h3>{title || "Error"}</h3>
      <p>{description || "Something went wrong."}</p>
      {onRetry && (
        <button className="retry-btn" onClick={onRetry}>
          Try Again
        </button>
      )}
    </div>
  );
}
