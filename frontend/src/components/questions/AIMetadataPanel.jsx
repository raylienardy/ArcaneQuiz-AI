import MetadataCard from "./MetadataCard";
import MetadataItem from "./MetadataItem";
import { formatLatency, formatTimestamp } from "../../utils/metadataFormatter";

export default function AIMetadataPanel({ metadata }) {
  if (!metadata) {
    return (
      <div className="ai-metadata-panel">
        <h3>AI Metadata</h3>
        <p className="metadata-unavailable">Metadata not available.</p>
      </div>
    );
  }

  const {
    provider,
    model,
    latency_seconds,
    prompt_version,
    schema_version,
    generation_timestamp,
    token_usage,
    finish_reason,
  } = metadata;

  return (
    <div className="ai-metadata-panel">
      <h3>AI Metadata</h3>
      <div className="metadata-cards">
        <MetadataCard title="Provider">
          <MetadataItem label="Provider" value={provider} />
          <MetadataItem label="Model" value={model} />
        </MetadataCard>
        <MetadataCard title="Performance">
          <MetadataItem
            label="Latency"
            value={formatLatency(latency_seconds)}
          />
          {token_usage && (
            <MetadataItem
              label="Tokens (Prompt/Completion/Total)"
              value={`${token_usage.prompt_tokens} / ${token_usage.completion_tokens} / ${token_usage.total_tokens}`}
            />
          )}
          {finish_reason && (
            <MetadataItem label="Finish Reason" value={finish_reason} />
          )}
        </MetadataCard>
        <MetadataCard title="Version Info">
          <MetadataItem label="Prompt Version" value={prompt_version} />
          <MetadataItem label="Schema Version" value={schema_version} />
        </MetadataCard>
        <MetadataCard title="Generation">
          <MetadataItem
            label="Timestamp"
            value={formatTimestamp(generation_timestamp)}
          />
        </MetadataCard>
      </div>
    </div>
  );
}
