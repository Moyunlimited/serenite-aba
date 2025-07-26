from db import db

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    questions = db.Column(db.PickleType, nullable=False)  # Will store list of dicts

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "questions": self.questions
        }
