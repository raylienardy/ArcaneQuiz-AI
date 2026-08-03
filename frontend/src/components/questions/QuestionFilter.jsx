export default function QuestionFilter({ value, onChange, types }) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="filter-select"
    >
      <option value="">All Types</option>
      {types.map((type) => (
        <option key={type} value={type}>
          {type.replace("_", " ")}
        </option>
      ))}
    </select>
  );
}
