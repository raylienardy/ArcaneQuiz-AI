export default function ExportWarnings({ warnings }) {
  if (!warnings || warnings.length === 0) return null;
  return (
    <div className="export-warnings">
      <h4>⚠️ Warnings</h4>
      <ul>
        {warnings.map((w, i) => (
          <li key={i}>{w}</li>
        ))}
      </ul>
    </div>
  );
}
