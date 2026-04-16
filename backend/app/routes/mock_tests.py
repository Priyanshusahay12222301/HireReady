from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.mock_test import MockTest
from app.models.mock_test_attempt import MockTestAttempt
from app.services.seed_data import ensure_seed_data

mock_tests_bp = Blueprint("mock_tests", __name__)


@mock_tests_bp.get("/mock-tests")
def list_mock_tests():
    ensure_seed_data()
    tests = MockTest.query.order_by(MockTest.id.asc()).all()
    return jsonify([test.to_dict() for test in tests]), 200


@mock_tests_bp.get("/mock-tests/<int:test_id>")
def get_mock_test(test_id):
    ensure_seed_data()
    test = MockTest.query.get_or_404(test_id)

    question_payload = [
        link.question.to_dict()
        for link in test.questions
        if link.question is not None
    ]

    return jsonify({"test": test.to_dict(), "questions": question_payload}), 200


@mock_tests_bp.post("/mock-tests/<int:test_id>/submit")
def submit_mock_test(test_id):
    ensure_seed_data()
    payload = request.get_json(silent=True) or {}

    user_id = payload.get("user_id")
    answers = payload.get("answers", [])
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    test = MockTest.query.get_or_404(test_id)
    answer_map = {}
    for entry in answers:
        question_id = entry.get("question_id")
        selected = entry.get("selected")
        if question_id is not None and selected:
            answer_map[int(question_id)] = str(selected).upper()

    correct = 0
    total = len(test.questions)
    details = []
    unanswered_count = 0
    for link in test.questions:
        question = link.question
        if not question:
            continue

        selected = answer_map.get(question.id)
        if not selected:
            unanswered_count += 1

        is_correct = selected == question.correct_option
        if is_correct:
            correct += 1

        details.append(
            {
                "question_id": question.id,
                "prompt": question.prompt,
                "selected": selected,
                "correct_option": question.correct_option,
                "is_correct": is_correct,
                "explanation": question.explanation,
            }
        )

    score_percent = round((correct / total) * 100, 2) if total else 0.0
    wrong_count = max(total - correct - unanswered_count, 0)

    attempt = MockTestAttempt(
        user_id=user_id,
        mock_test_id=test.id,
        correct_count=correct,
        total_questions=total,
        score_percent=score_percent,
    )
    db.session.add(attempt)
    db.session.commit()

    attempt_count = MockTestAttempt.query.filter_by(user_id=user_id, mock_test_id=test.id).count()

    return jsonify(
        {
            "attempt": attempt.to_dict(),
            "attempt_count": attempt_count,
            "result": {
                "correct_count": correct,
                "wrong_count": wrong_count,
                "unanswered_count": unanswered_count,
                "total_questions": total,
                "score_percent": score_percent,
                "details": details,
            },
        }
    ), 201
