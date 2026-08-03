import "./UploadError.css";

export default function UploadError({ message, onRetry }) {
  return (
    <div className="upload-error">
      <span className="error-icon">❌</span>
      <h3>Upload Failed</h3>
      <div className="error-message-box">
        <p>{message}</p>
      </div>
      {onRetry && (
        <button className="retry-btn" onClick={onRetry}>
          Try Again
        </button>
      )}
    </div>
  );
}
