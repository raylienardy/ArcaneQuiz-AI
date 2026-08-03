export default function RawResponseViewer({ text }) {
  if (!text) return <div>No raw response.</div>;
  return (
    <div>
      <pre className="raw-text">{text}</pre>
    </div>
  );
}
