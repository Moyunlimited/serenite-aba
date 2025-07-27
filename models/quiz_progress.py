from db import db
from datetime import datetime

class QuizProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    quiz_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    quiz_title = db.Column(db.String(120))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "quiz_id": self.quiz_id,
            "score": self.score,
            "total": self.total,
            "quiz_title": self.quiz_title,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M")
        }
