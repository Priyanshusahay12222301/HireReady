from flask import Blueprint, jsonify, request
from typing import Optional

from app.extensions import bcrypt, db
from app.models.user import User
from app.services.cv_parser import parse_cv

auth_bp = Blueprint("auth", __name__)


def serialize_user(user: User, extra: Optional[dict] = None):
    data = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "roll_no": user.roll_no,
        "role": user.role,
        "cgpa": user.cgpa,
        "skills": user.skills,
        "phone": user.phone,
        "gender": user.gender,
        "branch": user.branch,
        "current_year": user.current_year,
    }
    if extra:
        data.update(extra)
    return data


def extract_register_payload():
    content_type = request.content_type or ""
    if "multipart/form-data" in content_type:
        name = request.form.get("name", "").strip()
        roll_no = request.form.get("roll_no", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        gender = request.form.get("gender", "").strip()
        branch = request.form.get("branch", "").strip()
        current_year = request.form.get("current_year", "").strip()
        cgpa_raw = request.form.get("cgpa", "").strip()
        cv_file = request.files.get("cv_file")
    else:
        payload = request.get_json(silent=True) or {}
        name = payload.get("name", "").strip()
        roll_no = payload.get("roll_no", "").strip()
        email = payload.get("email", "").strip().lower()
        password = payload.get("password", "")
        gender = payload.get("gender", "").strip()
        branch = str(payload.get("branch", "")).strip()
        current_year = str(payload.get("current_year", "")).strip()
        cgpa_raw = str(payload.get("cgpa", "")).strip()
        cv_file = None

    cgpa = None
    if cgpa_raw:
        try:
            cgpa = float(cgpa_raw)
        except ValueError:
            cgpa = None

    return name, roll_no, email, password, gender, branch, current_year, cgpa, cv_file


@auth_bp.post("/register")
def register():
    name, roll_no, email, password, gender, branch, current_year, cgpa, cv_file = extract_register_payload()

    if not all([name, roll_no, email, password, gender]):
        return jsonify({"error": "name, roll_no, email, password, and gender are required"}), 400

    normalized_gender = gender.lower()
    if normalized_gender not in {"male", "female", "other"}:
        return jsonify({"error": "gender must be one of: male, female, other"}), 400

    if cgpa is not None and (cgpa < 0 or cgpa > 10):
        return jsonify({"error": "cgpa must be between 0 and 10"}), 400

    if User.query.filter((User.email == email) | (User.roll_no == roll_no)).first():
        return jsonify({"error": "email or roll number already exists"}), 409

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(
        name=name,
        roll_no=roll_no,
        email=email,
        password_hash=password_hash,
        gender=normalized_gender,
    )
    parsed = {"phone": None, "branch": None, "current_year": None}

    if cv_file and cv_file.filename:
        parsed = parse_cv(cv_file)
        user.skills = parsed.get("skills")
        user.phone = parsed.get("phone")

        parsed_cgpa = parsed.get("cgpa")
        parsed_branch = parsed.get("branch")
        parsed_year = parsed.get("current_year")

        user.cgpa = cgpa if cgpa is not None else parsed_cgpa
        user.branch = branch or parsed_branch
        user.current_year = current_year or parsed_year
    else:
        user.cgpa = cgpa
        user.branch = branch or None
        user.current_year = current_year or None

    db.session.add(user)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "registration successful",
                "user": serialize_user(
                    user,
                    {
                        "phone": parsed.get("phone"),
                        "branch": parsed.get("branch"),
                        "current_year": parsed.get("current_year"),
                    },
                ),
            }
        ),
        201,
    )


@auth_bp.post("/login")
def login():
    payload = request.get_json(silent=True) or {}
    identifier = payload.get("identifier", "").strip().lower()
    password = payload.get("password", "")

    if not identifier or not password:
        return jsonify({"error": "identifier and password are required"}), 400

    user = User.query.filter((User.email == identifier) | (User.roll_no == identifier)).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error": "invalid credentials"}), 401

    return jsonify(
        {
            "message": "login successful",
            "user": serialize_user(user),
        }
    ), 200


@auth_bp.post("/users/<int:user_id>/resume")
def upload_resume(user_id: int):
    user = User.query.get_or_404(user_id)
    cv_file = request.files.get("cv_file")

    if not cv_file or not cv_file.filename:
        return jsonify({"error": "cv_file is required"}), 400

    filename = cv_file.filename.lower()
    if not filename.endswith((".pdf", ".doc", ".docx")):
        return jsonify({"error": "Only PDF, DOC, and DOCX files are supported"}), 400

    parsed = parse_cv(cv_file)
    user.cgpa = parsed.get("cgpa")
    user.skills = parsed.get("skills")
    user.phone = parsed.get("phone")
    user.branch = parsed.get("branch")
    user.current_year = parsed.get("current_year")

    db.session.commit()

    return jsonify({"message": "resume updated successfully", "user": serialize_user(user)}), 200


@auth_bp.patch("/users/<int:user_id>")
def update_user_profile(user_id: int):
    user = User.query.get_or_404(user_id)
    payload = request.get_json(silent=True) or {}

    name = str(payload.get("name", user.name)).strip()
    phone = str(payload.get("phone", user.phone or "")).strip() or None
    gender = str(payload.get("gender", user.gender or "")).strip().lower()
    branch = str(payload.get("branch", user.branch or "")).strip() or None
    current_year = str(payload.get("current_year", user.current_year or "")).strip() or None

    if not name:
        return jsonify({"error": "name is required"}), 400

    if gender and gender not in {"male", "female", "other"}:
        return jsonify({"error": "gender must be one of: male, female, other"}), 400

    user.name = name
    user.phone = phone
    user.gender = gender or None
    user.branch = branch
    user.current_year = current_year

    db.session.commit()

    return jsonify({"message": "profile updated successfully", "user": serialize_user(user)}), 200
