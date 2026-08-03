import { useState } from "react";
import ExportSummary from "./ExportSummary";
import ExportMetadataPanel from "./ExportMetadataPanel";
import ExportWarnings from "./ExportWarnings";
import ExportDownloadButton from "./ExportDownloadButton";

export default function ExportPreview({ previewData, onDownload }) {
  if (!previewData) return null;

  return (
    <div className="export-preview">
      <h3>Export Preview</h3>
      <ExportSummary
        filename={previewData.filename}
        format={previewData.format}
        estimatedSize={previewData.estimated_size_human}
        estimatedPages={previewData.estimated_pages}
        questionCount={previewData.question_count}
      />
      <ExportMetadataPanel metadata={previewData.metadata} />
      <ExportWarnings warnings={previewData.warnings} />
      <ExportDownloadButton onDownload={onDownload} />
    </div>
  );
}
