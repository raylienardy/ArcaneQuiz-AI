import { useState } from "react";
import { formatJSON } from "../../utils/export/jsonFormatter";
import { formatMarkdown } from "../../utils/export/markdownFormatter";
import { formatQuestionsOnly } from "../../utils/export/plainTextFormatter";
import { copyToClipboard } from "../../utils/export/clipboard";

export default function QuestionToolbar({ questions, onRegenerate }) {
  const [copyStatus, setCopyStatus] = useState("");

  const handleCopy = async (formatFn) => {
    try {
      const text = formatFn(questions);
      const success = await copyToClipboard(text);
      if (success) {
        setCopyStatus("Copied!");
        setTimeout(() => setCopyStatus(""), 2000);
      } else {
        setCopyStatus("Failed to copy.");
        setTimeout(() => setCopyStatus(""), 3000);
      }
    } catch {
      setCopyStatus("Error preparing data.");
      setTimeout(() => setCopyStatus(""), 3000);
    }
  };

  const handleDownloadJSON = () => {
    const json = formatJSON(questions);
    const blob = new Blob([json], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "questions.json";
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="question-toolbar">
      <button onClick={onRegenerate} className="toolbar-btn">
        🔄 Regenerate
      </button>
      <button onClick={() => handleCopy(formatJSON)} className="toolbar-btn">
        📋 Copy JSON
      </button>
      <button
        onClick={() => handleCopy(formatMarkdown)}
        className="toolbar-btn"
      >
        📋 Copy Markdown
      </button>
      <button
        onClick={() => handleCopy(formatQuestionsOnly)}
        className="toolbar-btn"
      >
        📋 Copy Questions Only
      </button>
      <button onClick={handleDownloadJSON} className="toolbar-btn">
        💾 Download JSON
      </button>
      {copyStatus && <span className="copy-feedback">{copyStatus}</span>}
    </div>
  );
}
