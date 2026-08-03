import FileDropzone from "./FileDropzone";
import SelectedFile from "./SelectedFile";
import LoadingSpinner from "./feedback/LoadingSpinner";
import ProgressBar from "./feedback/ProgressBar";
import UploadResult from "./feedback/UploadResult";
import UploadError from "./feedback/UploadError";
import DocumentPreview from "./preview/DocumentPreview";

export default function UploadCard({
  file,
  onFileSelect,
  onRemove,
  onUpload,
  uploadState,
  uploadResult,
  uploadError,
  validationError,
  onReset,
}) {
  const isIdle = uploadState === "idle";
  const isUploading = uploadState === "uploading";
  const isSuccess = uploadState === "success";
  const isError = uploadState === "error";

  return (
    <div className="upload-card">
      {!file && isIdle && <FileDropzone onFileSelect={onFileSelect} />}

      {file && !isSuccess && (
        <>
          <SelectedFile file={file} onRemove={isUploading ? null : onRemove} />
          {isIdle && validationError && (
            <div className="validation-message error">
              <span className="validation-icon">⚠️</span>
              <p>{validationError}</p>
            </div>
          )}
          {isIdle && !validationError && (
            <div className="validation-message success">
              <span className="validation-icon">✅</span>
              <p>Ready to upload</p>
            </div>
          )}
        </>
      )}

      {isUploading && (
        <div className="upload-feedback">
          <LoadingSpinner size={36} />
          <ProgressBar indeterminate />
          <p className="uploading-text">Extracting document... Please wait.</p>
        </div>
      )}

      {isSuccess && uploadResult && (
        <>
          <UploadResult
            fileInfo={{
              filename: uploadResult.filename,
              content_type: uploadResult.content_type,
              size: uploadResult.size,
            }}
            onReset={onReset}
          />
          {uploadResult.text != null && (
            <DocumentPreview result={uploadResult} />
          )}
        </>
      )}

      {isError && (
        <UploadError
          message={uploadError || "An unexpected error occurred."}
          onRetry={file ? onUpload : null}
        />
      )}

      {file && isIdle && !validationError && (
        <>
          <button className="arcane-btn upload-btn" onClick={onUpload}>
            Upload & Extract
          </button>
          <p className="upload-hint">Click to upload and extract text.</p>
        </>
      )}
    </div>
  );
}
