export default function QuestionAnswer({ answer }) {
  if (!answer) return null;
  return (
    <div className="detail-answer">
      <h4>Answer</h4>
      <p>{answer}</p>
    </div>
  );
}
