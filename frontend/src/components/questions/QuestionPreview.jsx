import QuestionCard from "./QuestionCard";
import QuestionToolbar from "./QuestionToolbar";

export default function QuestionPreview({
  questions,
  onRegenerate,
  isLoading,
  error,
}) {
  if (isLoading) {
    return (
      <div className="question-preview-container">
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Generating questions... Please wait.</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="question-preview-container">
        <div className="error-state">
          <p>❌ {error}</p>
          {onRegenerate && (
            <button onClick={onRegenerate} className="retry-btn">
              Try Again
            </button>
          )}
        </div>
      </div>
    );
  }

  if (!questions || questions.length === 0) {
    return (
      <div className="question-preview-container">
        <div className="empty-state">
          <p>No questions generated yet.</p>
          <p>Upload a document and generate questions.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="question-preview-container">
      <QuestionToolbar questions={questions} onRegenerate={onRegenerate} />
      <div className="questions-list">
        {questions.map((q, idx) => (
          <QuestionCard key={q.id || idx} question={q} index={idx} />
        ))}
      </div>
    </div>
  );
}
