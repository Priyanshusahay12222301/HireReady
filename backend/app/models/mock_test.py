from app.extensions import db


class MockTest(db.Model):
    __tablename__ = "mock_tests"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    company = db.Column(db.String(120), nullable=False, default="General")
    duration_minutes = db.Column(db.Integer, nullable=False, default=20)
    total_questions = db.Column(db.Integer, nullable=False, default=20)

    questions = db.relationship(
        "MockTestQuestion",
        back_populates="mock_test",
        cascade="all, delete-orphan",
        order_by="MockTestQuestion.position",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "duration_minutes": self.duration_minutes,
            "total_questions": self.total_questions,
        }


class MockTestQuestion(db.Model):
    __tablename__ = "mock_test_questions"

    id = db.Column(db.Integer, primary_key=True)
    mock_test_id = db.Column(db.Integer, db.ForeignKey("mock_tests.id"), nullable=False, index=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False, index=True)
    position = db.Column(db.Integer, nullable=False)

    mock_test = db.relationship("MockTest", back_populates="questions")
    question = db.relationship("Question")
