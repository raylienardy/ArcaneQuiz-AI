export default function ProgressIndicator({ indeterminate = true }) {
  return (
    <div className="progress-indicator">
      <div
        className={`progress-bar ${indeterminate ? "indeterminate" : ""}`}
      ></div>
    </div>
  );
}
