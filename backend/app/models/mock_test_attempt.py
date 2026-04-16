from datetime import datetime

from app.extensions import db


class MockTestAttempt(db.Model):
    __tablename__ = "mock_test_attempts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    mock_test_id = db.Column(db.Integer, db.ForeignKey("mock_tests.id"), nullable=False, index=True)
    correct_count = db.Column(db.Integer, nullable=False, default=0)
    total_questions = db.Column(db.Integer, nullable=False, default=0)
    score_percent = db.Column(db.Float, nullable=False, default=0.0)
    submitted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("User")
    mock_test = db.relationship("MockTest")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "mock_test_id": self.mock_test_id,
            "correct_count": self.correct_count,
            "total_questions": self.total_questions,
            "score_percent": self.score_percent,
            "submitted_at": self.submitted_at.isoformat() if self.submitted_at else None,
        }
