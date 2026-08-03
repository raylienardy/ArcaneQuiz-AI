import PipelineStep from "./PipelineStep";
import PromptViewer from "./PromptViewer";
import RawResponseViewer from "./RawResponseViewer";
import JSONViewer from "./JSONViewer";
import ValidationViewer from "./ValidationViewer";
import FinalResponseViewer from "./FinalResponseViewer";

export default function AIPipelineInspector({ debugData, isOpen }) {
  if (!isOpen || !debugData) return null;

  const steps = [
    {
      title: "Prompt Builder",
      status: debugData.prompt ? "success" : "error",
      render: () => <PromptViewer data={debugData.prompt} />,
    },
    {
      title: "AI Provider",
      status: debugData.provider
        ? debugData.provider.error
          ? "error"
          : "success"
        : "error",
      render: () => (
        <div>
          {debugData.provider ? (
            <>
              <div>Provider: {debugData.provider.provider}</div>
              <div>Model: {debugData.provider.model}</div>
              {debugData.provider.latency_seconds && (
                <div>Latency: {debugData.provider.latency_seconds}s</div>
              )}
              {debugData.provider.error && (
                <div className="error">Error: {debugData.provider.error}</div>
              )}
            </>
          ) : (
            <div>No provider info</div>
          )}
        </div>
      ),
    },
    {
      title: "Raw AI Response",
      status: debugData.raw_response ? "success" : "error",
      render: () => <RawResponseViewer text={debugData.raw_response} />,
    },
    {
      title: "Extracted JSON",
      status: debugData.parsed_json
        ? "success"
        : debugData.parser?.status === "failed"
          ? "error"
          : "pending",
      render: () => {
        if (debugData.parsed_json)
          return <JSONViewer data={debugData.parsed_json} />;
        if (debugData.parser?.error)
          return <div className="error">{debugData.parser.error}</div>;
        return <div>Not executed</div>;
      },
    },
    {
      title: "Validator",
      status:
        debugData.validation?.status === "passed"
          ? "success"
          : debugData.validation?.status === "failed"
            ? "error"
            : "pending",
      render: () => <ValidationViewer data={debugData.validation} />,
    },
    {
      title: "Final QuestionResponse",
      status: debugData.final_response ? "success" : "pending",
      render: () => <FinalResponseViewer data={debugData.final_response} />,
    },
  ];

  return (
    <div className="ai-pipeline-inspector">
      <h2>AI Pipeline Inspector</h2>
      {steps.map((step, idx) => (
        <PipelineStep
          key={idx}
          stepNumber={idx + 1}
          title={step.title}
          status={step.status}
        >
          {step.render()}
        </PipelineStep>
      ))}
    </div>
  );
}
