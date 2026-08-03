import { formatFileSize } from "../utils/formatFileSize";

function getFileIcon(fileName) {
  const ext = fileName?.split(".").pop()?.toLowerCase();
  switch (ext) {
    case "pdf":
      return "📄";
    case "docx":
      return "📝";
    case "txt":
      return "📃";
    default:
      return "📎";
  }
}

export default function SelectedFile({ file, onRemove }) {
  if (!file) return null;

  return (
    <div className="selected-file">
      <div className="file-info">
        <span className="file-icon">{getFileIcon(file.name)}</span>
        <div className="file-details">
          <p className="file-name">{file.name}</p>
          <p className="file-size">{formatFileSize(file.size)}</p>
        </div>
      </div>
      {onRemove && (
        <button className="remove-btn" onClick={onRemove} title="Remove file">
          ✕
        </button>
      )}
    </div>
  );
}
