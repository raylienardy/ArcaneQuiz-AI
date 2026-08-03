export default function ValidationViewer({ data }) {
  if (!data) return <div>No validation data.</div>;
  return (
    <div>
      <div>
        <strong>Status:</strong>{" "}
        {data.status === "passed" ? "✅ Passed" : "❌ Failed"}
      </div>
      {data.errors?.length > 0 && (
        <ul>
          {data.errors.map((err, i) => (
            <li key={i}>{err}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
