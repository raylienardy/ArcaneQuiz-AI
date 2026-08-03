import { useState } from "react";
import PreviewMetadata from "./PreviewMetadata";
import PreviewToolbar from "./PreviewToolbar";
import "./DocumentPreview.css";

const PREVIEW_LINES = 20; // jumlah baris yang ditampilkan saat collapsed

export default function DocumentPreview({ result }) {
  const [expanded, setExpanded] = useState(false);
  const text = result.text || "";
  const lines = text.split("\n");
  const collapsed = !expanded && lines.length > PREVIEW_LINES;

  const displayedText = collapsed
    ? lines.slice(0, PREVIEW_LINES).join("\n") + "\n..."
    : text;

  return (
    <div className="document-preview">
      <PreviewMetadata
        fileInfo={{ filename: result.filename, size: result.size }}
        charCount={result.character_count}
        wordCount={result.word_count}
        warnings={result.warnings}
      />
      <PreviewToolbar
        text={text}
        onToggleExpand={() => setExpanded(!expanded)}
        isExpanded={expanded}
      />
      <div className="preview-text-container">
        {text ? (
          <pre className="preview-text">{displayedText}</pre>
        ) : (
          <p className="no-text-message">
            No readable text was found in this document.
          </p>
        )}
      </div>
    </div>
  );
}
