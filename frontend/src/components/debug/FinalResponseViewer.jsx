import JSONViewer from "./JSONViewer";

export default function FinalResponseViewer({ data }) {
  if (!data) return <div>No final response.</div>;
  return <JSONViewer data={data} />;
}
