export default function QuestionExplanation({ explanation }) {
  if (!explanation) return null;
  return (
    <div className="detail-explanation">
      <h4>Explanation</h4>
      <p>{explanation}</p>
    </div>
  );
}
