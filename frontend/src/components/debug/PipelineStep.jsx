import { useState } from "react";

export default function PipelineStep({ stepNumber, title, status, children }) {
  const [expanded, setExpanded] = useState(false);
  const statusIcon =
    status === "success" ? "✅" : status === "error" ? "❌" : "⏸️";

  return (
    <div className="pipeline-step">
      <div className="step-header" onClick={() => setExpanded(!expanded)}>
        <span className="step-number">{stepNumber}</span>
        <span className="step-title">{title}</span>
        <span className="step-status">{statusIcon}</span>
        <button>{expanded ? "▼" : "▶"}</button>
      </div>
      {expanded && <div className="step-content">{children}</div>}
    </div>
  );
}
