from db import db

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content
        }
