export default function QuestionSearch({ value, onChange }) {
  return (
    <div className="search-container">
      <input
        type="text"
        placeholder="Search questions..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="search-input"
      />
    </div>
  );
}
