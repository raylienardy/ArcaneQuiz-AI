import SessionInfoItem from "./SessionInfoItem";
import { formatLatency, formatTimestamp } from "../../utils/metadataFormatter";

export default function GenerationSessionPanel({ session }) {
  if (!session) {
    return (
      <div className="generation-session-panel">
        <h3>Generation Session</h3>
        <p className="session-empty">No active generation session.</p>
      </div>
    );
  }

  return (
    <div className="generation-session-panel">
      <h3>Generation Session</h3>
      <div className="session-cards">
        <div className="session-card">
          <SessionInfoItem
            label="Generated At"
            value={formatTimestamp(session.generatedAt)}
          />
          <SessionInfoItem label="Status" value={session.status} />
          <SessionInfoItem label="Provider" value={session.provider} />
          <SessionInfoItem label="Model" value={session.model} />
        </div>
        <div className="session-card">
          <SessionInfoItem
            label="Question Count"
            value={session.questionCount}
          />
          <SessionInfoItem label="Question Type" value={session.questionType} />
          <SessionInfoItem label="Difficulty" value={session.difficulty} />
          <SessionInfoItem label="Language" value={session.language} />
        </div>
        <div className="session-card">
          <SessionInfoItem
            label="Generation Time"
            value={formatLatency(session.generationTime)}
          />
          <SessionInfoItem
            label="Prompt Version"
            value={session.promptVersion}
          />
          <SessionInfoItem
            label="Schema Version"
            value={session.schemaVersion}
          />
        </div>
      </div>
    </div>
  );
}
