export default function DeveloperToolbar({ devMode, onToggle }) {
  return (
    <div className="developer-toolbar">
      <label>
        <input
          type="checkbox"
          checked={devMode}
          onChange={(e) => onToggle(e.target.checked)}
        />
        Developer Mode
      </label>
      {devMode && <span className="dev-mode-indicator">🐞 Active</span>}
    </div>
  );
}
