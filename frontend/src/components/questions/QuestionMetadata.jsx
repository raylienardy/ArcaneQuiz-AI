export default function QuestionMetadata({ question }) {
  return (
    <div className="detail-metadata">
      {question.id && <span>ID: {question.id}</span>}
      {question.language && <span>Language: {question.language}</span>}
      {/* Tempat untuk metadata provider di masa depan */}
    </div>
  );
}
