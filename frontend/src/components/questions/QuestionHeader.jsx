export default function QuestionHeader({ question, index }) {
  return (
    <div className="detail-header">
      <span className="detail-number">Question {index + 1}</span>
      <span className="detail-type-badge">
        {question.type.replace("_", " ")}
      </span>
      {question.difficulty && (
        <span className="detail-difficulty">{question.difficulty}</span>
      )}
    </div>
  );
}
