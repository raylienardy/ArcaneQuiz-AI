export default function QuestionChoices({ choices, answer }) {
  if (!choices || choices.length === 0) return null;
  return (
    <div className="detail-choices">
      <h4>Choices</h4>
      {choices.map((choice, idx) => {
        const isCorrect = choice.label === answer || choice.text === answer;
        return (
          <div
            key={idx}
            className={`detail-choice ${isCorrect ? "correct" : ""}`}
          >
            <span className="choice-label">{choice.label}.</span>
            <span className="choice-text">{choice.text}</span>
          </div>
        );
      })}
    </div>
  );
}
