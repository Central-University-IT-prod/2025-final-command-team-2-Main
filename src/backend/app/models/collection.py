from app import db
from datetime import datetime, UTC

class Collection(db.Model):
    __tablename__ = 'collections'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))
    is_default = db.Column(db.Boolean, default=False)
    is_group_collection = db.Column(db.Boolean, default=False)
    group_id = db.Column(db.String(100), nullable=True)

    movies = db.relationship('Movie', secondary='collection_movies', backref=db.backref('collections', lazy='dynamic'))
    users = db.relationship('CollectionUser', backref='collection', cascade='all, delete-orphan')

    def to_dict(self):
        movies_with_notes = []
        for movie in self.movies:
            movie_data = movie.to_dict()
            movie_in_collection = db.session.query(collection_movies).filter_by(
                collection_id=self.id,
                movie_id=movie.id
            ).first()
            if movie_in_collection:
                movie_data['notes'] = movie_in_collection.notes
            movies_with_notes.append(movie_data)
            
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'isDefault': self.is_default,
            'isGroupCollection': self.is_group_collection,
            'groupId': self.group_id,
            'users': [user.to_dict() for user in self.users],
            'movies': movies_with_notes,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat()
        }

collection_movies = db.Table('collection_movies',
    db.Column('collection_id', db.Integer, db.ForeignKey('collections.id', ondelete='CASCADE'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id', ondelete='CASCADE'), primary_key=True),
    db.Column('added_at', db.DateTime, default=datetime.now(UTC)),
    db.Column('added_by', db.String(100), nullable=True),
    db.Column('notes', db.String(255), nullable=True)
)

class CollectionUser(db.Model):
    __tablename__ = 'collection_users'
    
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.id', ondelete='CASCADE'), primary_key=True)
    telegram_id = db.Column(db.Integer, db.ForeignKey('users.telegramId', ondelete='CASCADE'), primary_key=True)
    added_at = db.Column(db.DateTime, default=datetime.now(UTC))

    __table_args__ = (
        db.PrimaryKeyConstraint('collection_id', 'telegram_id'),
    )
    
    def to_dict(self):
        from app.models import User
        user = User.query.filter_by(telegramId=self.telegram_id).first()
        if not user:
            return None
        
        return {
            'userId': str(user.id),
            'telegramId': str(self.telegram_id),
            'username': user.username,
            'avatarUrl': user.avatarUrl,
            'addedAt': self.added_at.isoformat()
        }
