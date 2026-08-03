import { useState } from "react";

export default function PromptViewer({ data }) {
  const [show, setShow] = useState(false);
  if (!data) return <div>No prompt data.</div>;

  return (
    <div>
      <div>
        <strong>Version:</strong> {data.prompt_version}
      </div>
      <div>
        <strong>Language:</strong> {data.language}
      </div>
      <div>
        <strong>Type:</strong> {data.question_type}
      </div>
      <div>
        <strong>Difficulty:</strong> {data.difficulty ?? "N/A"}
      </div>
      <div>
        <strong>Questions:</strong> {data.question_count}
      </div>
      <button onClick={() => setShow(!show)}>
        {show ? "Hide" : "Show"} Prompt
      </button>
      {show && <pre className="raw-text">{data.text}</pre>}
    </div>
  );
}
