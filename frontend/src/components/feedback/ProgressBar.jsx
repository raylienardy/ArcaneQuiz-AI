import "./ProgressBar.css";

export default function ProgressBar({ indeterminate = true }) {
  return (
    <div className="progress-bar-container">
      <div
        className={`progress-bar-fill ${indeterminate ? "indeterminate" : ""}`}
      ></div>
    </div>
  );
}
