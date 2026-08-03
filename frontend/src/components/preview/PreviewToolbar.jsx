import { useState } from "react";

export default function PreviewToolbar({ text, onToggleExpand, isExpanded }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // fallback jika clipboard API tidak didukung
      const textarea = document.createElement("textarea");
      textarea.value = text;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand("copy");
      document.body.removeChild(textarea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="preview-toolbar">
      <button onClick={handleCopy} className="toolbar-btn">
        {copied ? "✅ Copied!" : "📋 Copy"}
      </button>
      <button onClick={onToggleExpand} className="toolbar-btn">
        {isExpanded ? "📕 Collapse" : "📖 Expand"}
      </button>
    </div>
  );
}
