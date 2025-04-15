from flask import Blueprint, jsonify, request
from app.models import Collection, CollectionUser, User, Movie
from app.models.collection import collection_movies
from app import db
from datetime import datetime, UTC
from pydantic import BaseModel, Field
from typing import List, Optional
from app.helpers import check_token
import random

collection_bp = Blueprint('collection', __name__)

class CollectionUserRequest(BaseModel):
    telegramId: int

class CreateCollectionRequest(BaseModel):
    name: str
    description: str
    isDefault: bool = False
    initialUsers: List[CollectionUserRequest] = []

class AddMovieRequest(BaseModel):
    movieId: int
    notes: Optional[str] = None

@collection_bp.route('/', methods=['POST'])
@check_token
def create_collection(user):
    if not user:
        return jsonify({
            'code': 403,
            'message': 'Forbidden'
        }), 404
    
    try:
        data = request.get_json()
        collection_data = CreateCollectionRequest(**data)
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': 'Invalid request data',
            'details': {
                'errors': str(e)
            }
        }), 400
    
    group_id = data.get('group_id')
    if not group_id and len(collection_data.initialUsers) > 0:
        group_id = f"group_{datetime.now(UTC).timestamp()}"
    
    new_collection = Collection(
        name=collection_data.name,
        description=collection_data.description,
        is_default=collection_data.isDefault,
        is_group_collection=len(collection_data.initialUsers) > 0,
        group_id=group_id
    )
    
    db.session.add(new_collection)
    db.session.flush()
    
    owner = CollectionUser(
        collection_id=new_collection.id,
        telegram_id=user.telegramId
    )
    db.session.add(owner)
    
    for user_data in collection_data.initialUsers:
        if user_data.telegramId == user.telegramId:
            continue
            
        if User.query.filter_by(telegramId=user_data.telegramId).first():
            collection_user = CollectionUser(
                collection_id=new_collection.id,
                telegram_id=user_data.telegramId
            )
            db.session.add(collection_user)
    
    db.session.commit()
    
    return jsonify(new_collection.to_dict()), 201

@collection_bp.route('/', methods=['GET'])
@check_token
def get_user_collections(user):
    if not user:
        return jsonify({
            'code': 403,
            'message': 'Forbidden'
        }), 403
    
    user_collections = Collection.query.join(
        CollectionUser, Collection.id == CollectionUser.collection_id
    ).filter(
        CollectionUser.telegram_id == user.telegramId
    ).all()
    
    if not user_collections:
        return jsonify([]), 200
    
    collections_data = []
    for collection in user_collections:
        collections_data.append(collection.to_dict())
    
    return jsonify(collections_data), 200

@collection_bp.route('/<int:collection_id>', methods=['GET'])
@check_token
def get_collection(user, collection_id):
    if not user:
        return jsonify({
            'code': 403,
            'message': 'Forbidden'
        }), 403
    
    collection = Collection.query.filter_by(id=collection_id).first()
    
    if not collection:
        return jsonify({
            'code': 404,
            'message': 'Collection not found'
        }), 404
    
    user_access = CollectionUser.query.filter_by(
        collection_id=collection_id,
        telegram_id=user.telegramId
    ).first()
    
    if not user_access:
        return jsonify({
            'code': 403,
            'message': 'You do not have access to this collection'
        }), 403
    
    return jsonify(collection.to_dict()), 200

@collection_bp.route('/<int:collection_id>', methods=['PUT'])
@check_token
def update_collection(user, collection_id):
    if not user:
        return jsonify({
            'code': 403,
            'message': 'Forbidden'
        }), 403
    
    collection = Collection.query.filter_by(id=collection_id).first()
    
    if not collection:
        return jsonify({
            'code': 404,
            'message': 'Collection not found'
        }), 404
    
    user_access = CollectionUser.query.filter_by(
        collection_id=collection_id,
        telegram_id=user.telegramId
    ).first()
    
    if not user_access:
        return jsonify({
            'code': 403,
            'message': 'You do not have access to this collection'
        }), 403
    
    data = request.json
    
    if 'name' in data:
        collection.name = data['name']
    
    if 'description' in data:
        collection.description = data['description']
    
    if 'isDefault' in data:
        collection.is_default = data['isDefault']
    
    db.session.commit()
    
    return jsonify(collection.to_dict()), 200

@collection_bp.route('/<int:collection_id>', methods=['DELETE'])
@check_token
def delete_collection(user, collection_id):
    if not user:
        return jsonify({
            'code': 403,
            'message': 'Forbidden'
        }), 403
    
    collection = Collection.query.filter_by(id=collection_id).first()
    
    if not collection:
        return jsonify({
            'code': 404,
            'message': 'Collection not found'
        }), 404
    
    user_access = CollectionUser.query.filter_by(
        collection_id=collection_id,
        telegram_id=user.telegramId
    ).first()
    
    if not user_access:
        return jsonify({
            'code': 403,
            'message': 'You do not have access to this collection'
        }), 403
    
    db.session.delete(collection)
    db.session.commit()
    
    return '', 204

@collection_bp.route('/<int:collection_id>/movies', methods=['POST'])
@check_token
def add_movie_to_collection(user, collection_id):
    if not user:
        return jsonify({
            'code': 403,
            'message': 'Forbidden'
        }), 403
    
    collection = Collection.query.filter_by(id=collection_id).first()
    
    if not collection:
        return jsonify({
            'code': 404,
            'message': 'Collection not found'
        }), 404
    
    user_access = CollectionUser.query.filter_by(
        collection_id=collection_id,
        telegram_id=user.telegramId
    ).first()
    
    if not user_access:
        return jsonify({
            'code': 403,
            'message': 'You do not have access to this collection'
        }), 403
    
    try:
        data = request.get_json()
        movie_data = AddMovieRequest(**data)
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': 'Invalid request data',
            'details': {
                'errors': str(e)
            }
        }), 400
    
    movie = Movie.query.filter_by(id=movie_data.movieId).first()
    
    if not movie:
        return jsonify({
            'code': 404,
            'message': 'Movie not found'
        }), 404
    
    if movie in collection.movies:
        return jsonify({
            'code': 400,
            'message': 'Movie already in collection'
        }), 400
    
    asd = db.insert(collection_movies).values(
        collection_id=collection.id,
        movie_id=movie.id,
        added_by=str(user.telegramId),
        notes=movie_data.notes
    )
    db.session.execute(asd)
    db.session.commit()
    
    return jsonify(collection.to_dict()), 200

@collection_bp.route('/<int:collection_id>/movies/<int:movie_id>', methods=['DELETE'])
@check_token
def remove_movie_from_collection(user, collection_id, movie_id):
    if not user:
        return jsonify({
            'code': 403,
            'message': 'Forbidden'
        }), 403
    
    collection = Collection.query.filter_by(id=collection_id).first()
    
    if not collection:
        return jsonify({
            'code': 404,
            'message': 'Collection not found'
        }), 404
    
    user_access = CollectionUser.query.filter_by(
        collection_id=collection_id,
        telegram_id=user.telegramId
    ).first()
    
    if not user_access:
        return jsonify({
            'code': 403,
            'message': 'You do not have access to this collection'
        }), 403
    
    movie = Movie.query.filter_by(id=movie_id).first()
    
    if not movie:
        return jsonify({
            'code': 404,
            'message': 'Movie not found'
        }), 404
    
    movie_in_collection = db.session.query(collection_movies).filter_by(
        collection_id=collection_id,
        movie_id=movie_id
    ).first()
    
    if not movie_in_collection:
        return jsonify({
            'code': 404,
            'message': 'Movie not found in this collection'
        }), 404
    
    db.session.execute(
        db.delete(collection_movies).where(
            (collection_movies.c.collection_id == collection_id) &
            (collection_movies.c.movie_id == movie_id)
        )
    )
    db.session.commit()
    
    return '', 204

@collection_bp.route('/<int:collection_id>/movies/<int:movie_id>', methods=['PUT'])
@check_token
def update_movie_notes(user, collection_id, movie_id):
    if not user:
        return jsonify({
            'code': 403,
            'message': 'Forbidden'
        }), 403
    
    collection = Collection.query.filter_by(id=collection_id).first()
    
    if not collection:
        return jsonify({
            'code': 404,
            'message': 'Collection not found'
        }), 404
    
    user_access = CollectionUser.query.filter_by(
        collection_id=collection_id,
        telegram_id=user.telegramId
    ).first()
    
    if not user_access:
        return jsonify({
            'code': 403,
            'message': 'You do not have access to this collection'
        }), 403
    
    movie = Movie.query.filter_by(id=movie_id).first()
    
    if not movie:
        return jsonify({
            'code': 404,
            'message': 'Movie not found'
        }), 404
    
    movie_in_collection = db.session.query(collection_movies).filter_by(
        collection_id=collection_id,
        movie_id=movie_id
    ).first()
    
    if not movie_in_collection:
        return jsonify({
            'code': 404,
            'message': 'Movie not found in this collection'
        }), 404
    
    data = request.get_json()
    notes = data.get('notes')
    
    db.session.execute(
        db.update(collection_movies)
        .where(
            (collection_movies.c.collection_id == collection_id) &
            (collection_movies.c.movie_id == movie_id)
        )
        .values(notes=notes)
    )
    db.session.commit()
    
    return jsonify({
        'message': 'Notes updated successfully'
    }), 200

@collection_bp.route('/<int:collection_id>/random', methods=['GET'])
@check_token
def get_random_movie_from_collection(user, collection_id):
    if not user:
        return jsonify({
            'code': 403,
            'message': 'Forbidden'
        }), 403
    
    collection = Collection.query.filter_by(id=collection_id).first()
    
    if not collection:
        return jsonify({
            'code': 404,
            'message': 'Collection not found'
        }), 404
    
    user_access = CollectionUser.query.filter_by(
        collection_id=collection_id,
        telegram_id=user.telegramId
    ).first()
    
    if not user_access:
        return jsonify({
            'code': 403,
            'message': 'You do not have access to this collection'
        }), 403
    
    if not collection.movies:
        return jsonify({
            'code': 404,
            'message': 'Collection is empty'
        }), 404
    
    random_movie = random.choice(collection.movies)
    movie_data = random_movie.to_dict()
    
    movie_in_collection = db.session.query(collection_movies).filter_by(
        collection_id=collection_id,
        movie_id=random_movie.id
    ).first()
    
    if movie_in_collection:
        movie_data['notes'] = movie_in_collection.notes
        movie_data['createdAt'] = movie_in_collection.added_at.isoformat()
        movie_data['createdBy'] = movie_in_collection.added_by
    
    return jsonify(movie_data), 200

@collection_bp.route('/<int:collection_id>/users', methods=['GET'])
@check_token
def get_collection_users(user, collection_id):
    if not user:
        return jsonify({
            'code': 403,
            'message': 'Forbidden'
        }), 403
    
    collection = Collection.query.filter_by(id=collection_id).first()
    
    if not collection:
        return jsonify({
            'code': 404,
            'message': 'Collection not found'
        }), 404
    
    user_access = CollectionUser.query.filter_by(
        collection_id=collection_id,
        telegram_id=user.telegramId
    ).first()
    
    if not user_access:
        return jsonify({
            'code': 403,
            'message': 'You do not have access to this collection'
        }), 403
    
    collection_users = CollectionUser.query.filter_by(collection_id=collection_id).all()
    users_data = []
    
    for collection_user in collection_users:
        user_data = collection_user.to_dict()
        if user_data:
            users_data.append(user_data)
    
    return jsonify(users_data), 200
@collection_bp.route('/<int:collection_id>/users', methods=['POST'])
@check_token
def add_user_to_collection(user, collection_id):
    if not user:
        return jsonify({
            'code': 403,
            'message': 'Forbidden'
        }), 403
    
    collection = Collection.query.filter_by(id=collection_id).first()
    
    if not collection:
        return jsonify({
            'code': 404,
            'message': 'Collection not found'
        }), 404
    
    user_access = CollectionUser.query.filter_by(
        collection_id=collection_id,
        telegram_id=user.telegramId
    ).first()
    
    if not user_access:
        return jsonify({
            'code': 403,
            'message': 'You do not have access to this collection'
        }), 403
    
    data = request.get_json()
    if not data or 'userTelegramId' not in data:
        return jsonify({
            'code': 400,
            'message': 'Missing userTelegramId in request'
        }), 400
    
    new_user_telegram_id = data['userTelegramId']
    
    new_user = User.query.filter_by(telegramId=new_user_telegram_id).first()
    if not new_user:
        return jsonify({
            'code': 404,
            'message': 'User not found'
        }), 404
    
    existing_user = CollectionUser.query.filter_by(
        collection_id=collection_id,
        telegram_id=new_user_telegram_id
    ).first()
    
    if existing_user:
        return jsonify({
            'code': 400,
            'message': 'User is already in this collection'
        }), 400
    
    new_collection_user = CollectionUser(
        collection_id=collection_id,
        telegram_id=new_user_telegram_id
    )
    
    db.session.add(new_collection_user)
    db.session.commit()
    
    return jsonify({
        'message': 'User successfully added to collection',
        'user': new_collection_user.to_dict()
    }), 200

@collection_bp.route('/<int:collection_id>/users/<int:user_telegram_id>', methods=['DELETE'])
@check_token
def remove_user_from_collection(user, collection_id, user_telegram_id):
    if not user:
        return jsonify({
            'code': 403,
            'message': 'Forbidden'
        }), 403
    
    collection = Collection.query.get(collection_id)
    if not collection:
        return jsonify({
            'code': 404,
            'message': 'Collection not found'
        }), 404
    
    user_access = CollectionUser.query.filter_by(
        collection_id=collection_id,
        telegram_id=user.telegramId
    ).first()
    
    if not user_access:
        return jsonify({
            'code': 403,
            'message': 'You do not have access to this collection'
        }), 403
    
    user_to_remove = CollectionUser.query.filter_by(
        collection_id=collection_id,
        telegram_id=user_telegram_id
    ).first()
    
    if not user_to_remove:
        return jsonify({
            'code': 404,
            'message': 'User not found in this collection'
        }), 404
    
    db.session.delete(user_to_remove)
    db.session.commit()
    
    return '', 204

