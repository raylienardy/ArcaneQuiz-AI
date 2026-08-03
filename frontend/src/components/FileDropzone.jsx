import { useRef, useState } from "react";

export default function FileDropzone({ onFileSelect }) {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const files = e.dataTransfer.files;
    if (files.length > 0 && onFileSelect) {
      onFileSelect(files[0]);
    }
  };

  const handleBrowse = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e) => {
    const files = e.target.files;
    if (files.length > 0 && onFileSelect) {
      onFileSelect(files[0]);
    }
    e.target.value = "";
  };

  return (
    <div
      className={`dropzone ${isDragging ? "dropzone-active" : ""}`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={handleBrowse}
    >
      <div className="dropzone-content">
        <div className="dropzone-icon">📁</div>
        <p className="dropzone-text">Drag & Drop your learning material here</p>
        <p className="dropzone-divider">or</p>
        <button type="button" className="browse-btn">
          Browse Files
        </button>
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept=".pdf,.docx,.txt"
          style={{ display: "none" }}
        />
      </div>
    </div>
  );
}
