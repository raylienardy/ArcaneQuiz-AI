export default function ExportSessionCard({ session }) {
  if (!session) return null;
  return (
    <div className="export-session-card">
      <h4>Export Session</h4>
      <div>Session ID: {session.session_id}</div>
      <div>Status: {session.status}</div>
      <div>Created: {new Date(session.created_at).toLocaleTimeString()}</div>
      {session.download_completed_at && (
        <div>
          Download Completed:{" "}
          {new Date(session.download_completed_at).toLocaleTimeString()}
        </div>
      )}
    </div>
  );
}
