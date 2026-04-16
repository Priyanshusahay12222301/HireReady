from flask import Blueprint, jsonify, request

from app.models.job import Job
from app.services.seed_data import ensure_seed_data

jobs_bp = Blueprint("jobs", __name__)


@jobs_bp.get("/jobs")
def get_jobs():
    ensure_seed_data()

    company = request.args.get("company")
    status = request.args.get("status")

    query = Job.query
    if company:
        query = query.filter(Job.company.ilike(f"%{company}%"))
    if status:
        query = query.filter(Job.status.ilike(f"%{status}%"))

    jobs = query.order_by(Job.days_left.asc(), Job.id.asc()).all()
    return jsonify([job.to_dict() for job in jobs]), 200
