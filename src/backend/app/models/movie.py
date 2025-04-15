from enum import unique

from app import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    description = db.Column(db.Text)
    image_url = db.Column(db.String())
    image_base64 = db.Column(db.Text)
    rating = db.Column(db.Float)
    genre = db.Column(db.String())
    duration = db.Column(db.Integer)
    year = db.Column(db.Integer)
    user_added = db.Column(db.Boolean, default=False)
    loaded_from_tmdb = db.Column(db.Boolean, default=False)


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image_url': self.image_url,
            'image_base64': self.image_base64,
            'rating': self.rating,
            'genre': self.genre,
            'duration': self.duration,
            'year': self.year,
            'loaded_from_tmdb': self.loaded_from_tmdb
        }
