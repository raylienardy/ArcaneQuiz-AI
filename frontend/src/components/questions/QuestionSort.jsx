export default function QuestionSort({ value, onChange }) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="sort-select"
    >
      <option value="default">Default Order</option>
      <option value="question_asc">Question A-Z</option>
      <option value="question_desc">Question Z-A</option>
      <option value="type_asc">Type A-Z</option>
      <option value="type_desc">Type Z-A</option>
      <option value="difficulty_asc">Difficulty Easy → Hard</option>
      <option value="difficulty_desc">Difficulty Hard → Easy</option>
    </select>
  );
}
