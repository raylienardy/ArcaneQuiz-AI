export default function LoadingSpinner({ size = 32, color = "#0d6efd" }) {
  return (
    <div
      className="loading-spinner"
      style={{ width: size, height: size, borderTopColor: color }}
    ></div>
  );
}
