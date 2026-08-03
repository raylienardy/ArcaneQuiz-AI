export default function PreviewMetadata({
  fileInfo,
  charCount,
  wordCount,
  warnings,
}) {
  return (
    <div className="preview-metadata">
      {fileInfo && (
        <p>
          <strong>File:</strong> {fileInfo.filename} (
          {(fileInfo.size / 1024 / 1024).toFixed(2)} MB)
        </p>
      )}
      <p>
        <strong>Characters:</strong> {charCount} | <strong>Words:</strong>{" "}
        {wordCount}
      </p>
      {warnings && warnings.length > 0 && (
        <div className="preview-warnings">
          {warnings.map((w, i) => (
            <p key={i} className="warning-item">
              ⚠️ {w}
            </p>
          ))}
        </div>
      )}
    </div>
  );
}
