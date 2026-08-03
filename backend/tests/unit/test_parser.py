import pytest
from app.question_generator.json_parser import JSONResponseParser
from app.question_generator.exceptions import QuestionParserError, QuestionFormatError

parser = JSONResponseParser()

def test_parse_valid_multiple_choice():
    raw = '{"questions": [{"question": "What is AI?", "type": "multiple_choice", "choices": ["A", "B", "C", "D"], "answer": "A", "explanation": "test"}]}'
    result = parser.parse(raw)
    assert len(result.questions) == 1
    assert result.questions[0].type == "multiple_choice"

def test_parse_with_markdown_fence():
    raw = '```json\n{"questions": [{"question": "Test?", "type": "essay", "answer": "Answer"}]}\n```'
    result = parser.parse(raw)
    assert len(result.questions) == 1
    assert result.questions[0].type == "essay"

def test_parse_empty_string_raises():
    with pytest.raises(QuestionParserError):
        parser.parse("")

def test_parse_invalid_json_raises():
    with pytest.raises(QuestionFormatError):
        parser.parse("{bad json}")

def test_parse_missing_questions_key():
    with pytest.raises(QuestionFormatError):
        parser.parse('{"other": []}')