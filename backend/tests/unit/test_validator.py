import pytest
from app.question_generator.validators import QuestionValidator
from app.question_generator.models import QuestionResponse, Question, Choice, QuestionType
from app.question_generator.exceptions import QuestionValidationError

validator = QuestionValidator()

def make_mcq(choices=4, answer="A", question_text="Q1"):
    labels = ['A', 'B', 'C', 'D'][:choices]
    return Question(
        id=1,
        question=question_text,
        type=QuestionType.MULTIPLE_CHOICE,
        choices=[Choice(label=l, text=f"Option {l}") for l in labels],
        answer=answer,
        explanation="Explanation"
    )

def test_valid_mcq_passes():
    response = QuestionResponse(questions=[make_mcq()])
    validated = validator.validate(response)
    assert len(validated.questions) == 1

def test_mcq_wrong_choice_count_raises():
    response = QuestionResponse(questions=[make_mcq(choices=3)])
    with pytest.raises(QuestionValidationError, match="exactly 4 choices"):
        validator.validate(response)

def test_mcq_missing_answer_raises():
    q = make_mcq()
    q.answer = ""
    response = QuestionResponse(questions=[q])
    with pytest.raises(QuestionValidationError, match="answer is missing"):
        validator.validate(response)

def test_essay_with_choices_raises():
    q = Question(
        id=1,
        question="Why?",
        type=QuestionType.ESSAY,
        choices=[Choice(label="A", text="Option")],
        answer="Because"
    )
    with pytest.raises(QuestionValidationError, match="essay question should not have choices"):
        validator.validate(QuestionResponse(questions=[q]))

def test_true_false_wrong_choices_raises():
    q = Question(
        id=1,
        question="True?",
        type=QuestionType.TRUE_FALSE,
        choices=[Choice(label="True", text="True"), Choice(label="False", text="False"), Choice(label="Maybe", text="Maybe")],
        answer="True"
    )
    with pytest.raises(QuestionValidationError, match="exactly 2 choices"):
        validator.validate(QuestionResponse(questions=[q]))

def test_duplicate_question_text_raises():
    q1 = make_mcq(question_text="Same question")
    q2 = make_mcq(question_text="Same question")
    q2.id = 2   # <-- tambahkan agar tidak bentrok ID
    with pytest.raises(QuestionValidationError, match="duplicate question text"):
        validator.validate(QuestionResponse(questions=[q1, q2]))