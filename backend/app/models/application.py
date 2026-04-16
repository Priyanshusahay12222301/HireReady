from datetime import datetime

from app.extensions import db


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False, index=True)
    status = db.Column(db.String(40), nullable=False, default="Applied")
    applied_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("User")
    job = db.relationship("Job")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "job_id": self.job_id,
            "status": self.status,
            "applied_on": self.applied_on.isoformat() if self.applied_on else None,
            "job": self.job.to_dict() if self.job else None,
        }
