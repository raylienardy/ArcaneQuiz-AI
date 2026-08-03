export default function ExportDownloadButton({ downloadUrl, onDownload }) {
  return (
    <button className="download-btn" onClick={onDownload}>
      📥 Download
    </button>
  );
}
