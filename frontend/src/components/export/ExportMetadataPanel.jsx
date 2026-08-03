import SessionInfoItem from "../session/SessionInfoItem";

export default function ExportMetadataPanel({ metadata }) {
  if (!metadata) return null;
  return (
    <div className="export-metadata">
      <h4>Metadata</h4>
      <SessionInfoItem label="Provider" value={metadata.provider} />
      <SessionInfoItem label="Model" value={metadata.model} />
      <SessionInfoItem
        label="Generated At"
        value={new Date(metadata.generated_at).toLocaleString()}
      />
      <SessionInfoItem label="Language" value={metadata.language} />
      <SessionInfoItem label="Difficulty" value={metadata.difficulty} />
      <SessionInfoItem label="Prompt Version" value={metadata.prompt_version} />
      <SessionInfoItem label="Schema Version" value={metadata.schema_version} />
      <SessionInfoItem label="Session ID" value={metadata.session_id} />
      <SessionInfoItem label="Correlation ID" value={metadata.request_id} />
    </div>
  );
}
