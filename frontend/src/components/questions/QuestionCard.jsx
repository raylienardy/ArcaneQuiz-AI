import { useState } from "react";
import QuestionDetailPanel from "./QuestionDetailPanel";

export default function QuestionCard({
  question,
  index,
  isSelected,
  onSelect,
}) {
  const [expanded, setExpanded] = useState(false);

  const handleClick = () => {
    onSelect(question, index);
    setExpanded(!expanded);
  };

  return (
    <div className={`question-card ${isSelected ? "selected" : ""}`}>
      <div
        className="question-card-header"
        onClick={handleClick}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === "Enter") handleClick();
        }}
      >
        <div className="question-header">
          <span className="question-number">Q{index + 1}</span>
          <span className="question-type-badge">
            {question.type.replace("_", " ")}
          </span>
          {question.difficulty && (
            <span className="question-difficulty">{question.difficulty}</span>
          )}
        </div>
        <p className="question-text">
          {question.question.substring(0, 100)}
          {question.question.length > 100 ? "..." : ""}
        </p>
        <div className="question-answer-indicator">
          Answer: {question.answer}
        </div>
        <span className="expand-icon">{expanded ? "▲" : "▼"}</span>
      </div>
      {expanded && (
        <div className="question-detail-inline">
          <QuestionDetailPanel question={question} index={index} />
        </div>
      )}
    </div>
  );
}
