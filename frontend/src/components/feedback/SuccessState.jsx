export default function SuccessState({ message, onAction }) {
  return (
    <div className="success-state">
      <div className="success-icon">✅</div>
      <p>{message || "Operation completed successfully."}</p>
      {onAction && (
        <button onClick={onAction}>{onAction.label || "Continue"}</button>
      )}
    </div>
  );
}
