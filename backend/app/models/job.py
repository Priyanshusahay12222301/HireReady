from app.extensions import db


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(120), nullable=False, index=True)
    role = db.Column(db.String(160), nullable=False)
    job_type = db.Column(db.String(40), nullable=False, default="Full-time")
    location = db.Column(db.String(120), nullable=True)
    days_left = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(40), nullable=False, default="Open")

    def to_dict(self):
        return {
            "id": self.id,
            "company": self.company,
            "role": self.role,
            "job_type": self.job_type,
            "location": self.location,
            "days_left": self.days_left,
            "status": self.status,
        }
