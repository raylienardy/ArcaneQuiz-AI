import QuestionCard from "./QuestionCard";

export default function QuestionList({
  questions,
  onSelect,
  selectedQuestionId,
}) {
  if (!questions || questions.length === 0) return null;
  return (
    <div className="questions-list">
      {questions.map((q, idx) => (
        <QuestionCard
          key={q.id || idx}
          question={q}
          index={idx}
          isSelected={
            q.id ? q.id === selectedQuestionId : idx === selectedQuestionId
          }
          onSelect={onSelect}
        />
      ))}
    </div>
  );
}
