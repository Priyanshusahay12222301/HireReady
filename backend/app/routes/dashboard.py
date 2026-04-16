from flask import Blueprint, jsonify
from sqlalchemy import func

from app.models.application import Application
from app.models.mock_test_attempt import MockTestAttempt
from app.models.user import User
from app.services.readiness import compute_readiness_score
from app.services.seed_data import ensure_seed_data


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/dashboard/<int:user_id>")
def dashboard_summary(user_id):
    ensure_seed_data()
    user = User.query.get_or_404(user_id)

    tests_taken = MockTestAttempt.query.filter_by(user_id=user.id).count()
    avg_raw = (
        MockTestAttempt.query.with_entities(func.avg(MockTestAttempt.score_percent))
        .filter(MockTestAttempt.user_id == user.id)
        .scalar()
    )
    avg_score = round(float(avg_raw), 2) if avg_raw is not None else 0.0
    jobs_applied = Application.query.filter_by(user_id=user.id).count()

    profile_fields = [
        user.name,
        user.email,
        user.roll_no,
        user.cgpa,
        user.skills,
        user.phone,
        user.branch,
        user.current_year,
    ]
    filled_fields = sum(1 for value in profile_fields if value)
    profile_completion = round((filled_fields / len(profile_fields)) * 100, 2)

    test_readiness = min(tests_taken * 20, 100)
    mock_interview_score = 70
    readiness = compute_readiness_score(
        profile_completion,
        test_readiness,
        avg_score,
        mock_interview_score,
    )

    return jsonify(
        {
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "roll_no": user.roll_no,
            },
            "stats": {
                "profile_completion": profile_completion,
                "tests_taken": tests_taken,
                "avg_mock_test_score": avg_score,
                "jobs_applied": jobs_applied,
                "readiness_score": readiness,
            },
        }
    ), 200
