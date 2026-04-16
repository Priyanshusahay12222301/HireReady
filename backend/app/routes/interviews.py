from datetime import datetime

from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.interview_schedule import InterviewSchedule
from app.models.user import User

interviews_bp = Blueprint("interviews", __name__)


def parse_iso_datetime(value: str):
    if not value:
        return None
    text = str(value).strip()
    if text.endswith("Z"):
        text = text[:-1]
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


@interviews_bp.get("/interviews")
def list_interviews():
    user_id = request.args.get("user_id", type=int)

    query = InterviewSchedule.query
    if user_id:
        query = query.filter_by(user_id=user_id)

    interviews = query.order_by(InterviewSchedule.scheduled_at.asc(), InterviewSchedule.id.asc()).all()
    return jsonify([item.to_dict() for item in interviews]), 200


@interviews_bp.post("/interviews")
def create_interview():
    payload = request.get_json(silent=True) or {}

    user_id = payload.get("user_id")
    company = str(payload.get("company") or "").strip()
    role = str(payload.get("role") or "").strip()
    scheduled_at = parse_iso_datetime(payload.get("scheduled_at"))

    if not user_id or not company or not role or not scheduled_at:
        return jsonify({"error": "user_id, company, role and valid scheduled_at are required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    interview = InterviewSchedule(
        user_id=user_id,
        company=company,
        role=role,
        interview_type=str(payload.get("interview_type") or "Technical").strip() or "Technical",
        scheduled_at=scheduled_at,
        mode=str(payload.get("mode") or "Virtual").strip() or "Virtual",
        location=str(payload.get("location") or "").strip() or None,
        status=str(payload.get("status") or "Scheduled").strip() or "Scheduled",
        notes=str(payload.get("notes") or "").strip() or None,
    )

    db.session.add(interview)
    db.session.commit()
    return jsonify(interview.to_dict()), 201


@interviews_bp.patch("/interviews/<int:interview_id>")
def update_interview(interview_id: int):
    interview = InterviewSchedule.query.get(interview_id)
    if not interview:
        return jsonify({"error": "Interview schedule not found"}), 404

    payload = request.get_json(silent=True) or {}

    updatable_fields = ["company", "role", "interview_type", "mode", "location", "status", "notes"]
    for field in updatable_fields:
        if field in payload:
            value = str(payload.get(field) or "").strip()
            setattr(interview, field, value or None)

    if "scheduled_at" in payload:
        parsed_dt = parse_iso_datetime(payload.get("scheduled_at"))
        if not parsed_dt:
            return jsonify({"error": "scheduled_at must be a valid ISO datetime"}), 400
        interview.scheduled_at = parsed_dt

    if not interview.company or not interview.role or not interview.interview_type or not interview.mode or not interview.status:
        return jsonify({"error": "company, role, interview_type, mode and status cannot be empty"}), 400

    db.session.commit()
    return jsonify(interview.to_dict()), 200


@interviews_bp.delete("/interviews/<int:interview_id>")
def delete_interview(interview_id: int):
    interview = InterviewSchedule.query.get(interview_id)
    if not interview:
        return jsonify({"error": "Interview schedule not found"}), 404

    db.session.delete(interview)
    db.session.commit()
    return jsonify({"message": "Interview schedule deleted"}), 200
