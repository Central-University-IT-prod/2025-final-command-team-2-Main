from app import db
from datetime import datetime, UTC

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    telegramId = db.Column(db.Integer, unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    avatarUrl = db.Column(db.String(100), nullable=False)

    createdAt = db.Column(db.DateTime, default=datetime.now(UTC))

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'telegramId': self.telegramId,
            'avatarUrl': self.avatarUrl,
            'createdAt': self.createdAt.isoformat()
        }
