from flask import Blueprint, jsonify, request

from app.models.question import Question
from app.services.seed_data import ensure_seed_data

questions_bp = Blueprint("questions", __name__)


@questions_bp.get("/questions")
def get_questions():
    ensure_seed_data()

    company = request.args.get("company")
    category = request.args.get("category")
    difficulty = request.args.get("difficulty")
    include_answer_arg = (request.args.get("include_answer") or "true").strip().lower()
    include_answer = include_answer_arg in {"1", "true", "yes", "y"}

    query = Question.query
    if company:
        query = query.filter(Question.company.ilike(f"%{company}%"))
    if category:
        query = query.filter(Question.category.ilike(f"%{category}%"))
    if difficulty:
        query = query.filter(Question.difficulty.ilike(f"%{difficulty}%"))

    questions = query.order_by(Question.id.asc()).all()
    return jsonify([question.to_dict(include_answer=include_answer) for question in questions]), 200
