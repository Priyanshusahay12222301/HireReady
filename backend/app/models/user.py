from flask_login import UserMixin

from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    roll_no = db.Column(db.String(30), nullable=False, unique=True, index=True)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="student")
    cgpa = db.Column(db.Float, nullable=True)
    skills = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    branch = db.Column(db.String(120), nullable=True)
    current_year = db.Column(db.String(20), nullable=True)

    def get_id(self):
        return str(self.id)
