from datetime import datetime

from app.extensions import db


class InterviewSchedule(db.Model):
    __tablename__ = "interview_schedules"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    company = db.Column(db.String(120), nullable=False, index=True)
    role = db.Column(db.String(160), nullable=False)
    interview_type = db.Column(db.String(60), nullable=False, default="Technical")
    scheduled_at = db.Column(db.DateTime, nullable=False, index=True)
    mode = db.Column(db.String(40), nullable=False, default="Virtual")
    location = db.Column(db.String(160), nullable=True)
    status = db.Column(db.String(40), nullable=False, default="Scheduled")
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "company": self.company,
            "role": self.role,
            "interview_type": self.interview_type,
            "scheduled_at": self.scheduled_at.isoformat() if self.scheduled_at else None,
            "mode": self.mode,
            "location": self.location,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
