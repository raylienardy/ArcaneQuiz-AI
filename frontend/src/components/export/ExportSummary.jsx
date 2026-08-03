export default function ExportSummary({
  filename,
  format,
  estimatedSize,
  estimatedPages,
  questionCount,
}) {
  return (
    <div className="export-summary">
      <div className="summary-item">
        <span className="summary-label">Filename:</span>
        <span className="summary-value">{filename}</span>
      </div>
      <div className="summary-item">
        <span className="summary-label">Format:</span>
        <span className="summary-value">
          {format ? format.toUpperCase() : "—"}
        </span>
      </div>
      {estimatedSize && (
        <div className="summary-item">
          <span className="summary-label">Estimated Size:</span>
          <span className="summary-value">{estimatedSize}</span>
        </div>
      )}
      {estimatedPages && (
        <div className="summary-item">
          <span className="summary-label">Estimated Pages:</span>
          <span className="summary-value">{estimatedPages}</span>
        </div>
      )}
      <div className="summary-item">
        <span className="summary-label">Question Count:</span>
        <span className="summary-value">{questionCount}</span>
      </div>
    </div>
  );
}
