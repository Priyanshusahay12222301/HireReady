from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.application import Application
from app.models.job import Job
from app.models.user import User
from app.services.seed_data import ensure_seed_data

applications_bp = Blueprint("applications", __name__)


@applications_bp.get("/applications")
def list_applications():
    ensure_seed_data()
    user_id = request.args.get("user_id", type=int)

    query = Application.query
    if user_id:
        query = query.filter_by(user_id=user_id)

    applications = query.order_by(Application.applied_on.desc(), Application.id.desc()).all()
    return jsonify([application.to_dict() for application in applications]), 200


@applications_bp.post("/applications")
def apply_job():
    ensure_seed_data()
    payload = request.get_json(silent=True) or {}

    user_id = payload.get("user_id")
    job_id = payload.get("job_id")
    if not user_id or not job_id:
        return jsonify({"error": "user_id and job_id are required"}), 400

    user = User.query.get(user_id)
    job = Job.query.get(job_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    if not job:
        return jsonify({"error": "Job not found"}), 404

    existing = Application.query.filter_by(user_id=user_id, job_id=job_id).first()
    if existing:
        return jsonify({"error": "Already applied to this job"}), 409

    application = Application(user_id=user_id, job_id=job_id, status="Applied")
    db.session.add(application)
    db.session.commit()

    return jsonify(application.to_dict()), 201
