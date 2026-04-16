from app.extensions import db


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(120), nullable=False, index=True)
    category = db.Column(db.String(120), nullable=False, index=True)
    difficulty = db.Column(db.String(20), nullable=False, default="Medium")
    prompt = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.Text, nullable=False)
    option_b = db.Column(db.Text, nullable=False)
    option_c = db.Column(db.Text, nullable=False)
    option_d = db.Column(db.Text, nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)
    explanation = db.Column(db.Text, nullable=True)

    def to_dict(self, include_answer: bool = False):
        data = {
            "id": self.id,
            "company": self.company,
            "category": self.category,
            "difficulty": self.difficulty,
            "prompt": self.prompt,
            "options": {
                "A": self.option_a,
                "B": self.option_b,
                "C": self.option_c,
                "D": self.option_d,
            },
            "explanation": self.explanation,
        }
        if include_answer:
            data["correct_option"] = self.correct_option
        return data
