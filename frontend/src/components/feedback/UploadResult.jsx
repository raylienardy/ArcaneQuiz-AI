import "./UploadResult.css";

export default function UploadResult({ fileInfo, onReset }) {
  const sizeMB = (fileInfo.size / (1024 * 1024)).toFixed(2);
  return (
    <div className="upload-result">
      <span className="result-icon">✅</span>
      <h3>Upload Complete</h3>
      <div className="result-details">
        <p>
          <strong>Filename:</strong> {fileInfo.filename}
        </p>
        <p>
          <strong>Size:</strong> {sizeMB} MB
        </p>
        <p>
          <strong>Type:</strong> {fileInfo.content_type}
        </p>
      </div>
      <p className="next-step">Ready for Text Extraction</p>
      <button className="reset-btn" onClick={onReset}>
        Upload Another File
      </button>
    </div>
  );
}
