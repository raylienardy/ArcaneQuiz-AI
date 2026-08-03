import QuestionPlaceholder from "./QuestionPlaceholder";
import QuestionHeader from "./QuestionHeader";
import QuestionBody from "./QuestionBody";
import QuestionChoices from "./QuestionChoices";
import QuestionAnswer from "./QuestionAnswer";
import QuestionExplanation from "./QuestionExplanation";
import QuestionMetadata from "./QuestionMetadata";

export default function QuestionDetailPanel({ question, index }) {
  if (!question) {
    return (
      <div className="question-detail-panel">
        <QuestionPlaceholder />
      </div>
    );
  }

  return (
    <div className="question-detail-panel">
      <QuestionHeader question={question} index={index} />
      <QuestionBody text={question.question} />
      <QuestionChoices choices={question.choices} answer={question.answer} />
      <QuestionAnswer answer={question.answer} />
      <QuestionExplanation explanation={question.explanation} />
      <QuestionMetadata question={question} />
    </div>
  );
}
