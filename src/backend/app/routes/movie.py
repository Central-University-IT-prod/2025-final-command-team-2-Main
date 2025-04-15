from flask import Blueprint, request, jsonify

from app import db
from app.models import Movie
from app.helpers import check_token
from pydantic import BaseModel, Field

movie_bp = Blueprint('movie_bp', __name__)

class MovieAdd(BaseModel):
    title: str
    description: str = 'null'
    image_url: str = 'null'
    image_base64: str = None
    rating: float = -1
    genre: str = 'null'
    duration: int = -1
    year: int = -1
    user_added: bool = False
    loaded_from_tmdb: bool = False




@movie_bp.route('/', methods=['GET'])
@check_token
def get_all_movies(user):
    films: list[Movie] = Movie.query.all()
    return jsonify([i.to_dict() for i in films])


@movie_bp.route('/<movie_id>')
@check_token
def get_movie(user, movie_id):
    movie = db.session.get(Movie, movie_id)
    if not movie:
        return jsonify({'error': 'no such movie'}), 404
    return jsonify(movie.to_dict())


@movie_bp.route('/', methods=['POST'])
@check_token
def add_movie(user):
    data = request.get_json()
    try:
        data = MovieAdd(**data)
    except Exception as e:
        return jsonify({'error': 'missing data', 'more_info': str(e)}), 400

    movie = Movie.query.filter_by(title=data.title).first()
    if movie:
        return jsonify({'reason': 'you can not add this film, because it is already exists'}), 400

    movie = Movie()
    movie.title = data.title
    movie.description = data.description
    movie.image_url = data.image_url
    movie.image_base64 = data.image_base64
    movie.rating = data.rating
    movie.genre = data.genre
    movie.duration = data.duration
    movie.year = data.year
    movie.user_added = data.user_added
    movie.loaded_from_tmdb = data.loaded_from_tmdb

    db.session.add(movie)
    db.session.commit()

    return jsonify(movie.to_dict()), 200


@movie_bp.route('/<movie_id>', methods=['PUT'])
@check_token
def edit_movie(user, movie_id):
    data = request.get_json()
    try:
        data = MovieAdd(**data)
    except:
        return jsonify({'error': 'missing data'}), 400

    movie = db.session.get(Movie, movie_id)
    if not movie:
        return jsonify({'error': 'no such movie'}), 404
    movie.title = data.title
    movie.description = data.description
    movie.image_url = data.image_url
    movie.image_base64 = data.image_base64
    movie.rating = data.rating
    movie.genre = data.genre
    movie.duration = data.duration
    movie.year = data.year
    movie.user_added = data.user_added
    movie.loaded_from_tmdb = data.loaded_from_tmdb

    db.session.commit()

    return jsonify(movie.to_dict()), 200

@movie_bp.route('/<movie_id>', methods=['DELETE'])
@check_token
def delete_movie(user, movie_id):
    movie = db.session.get(Movie, movie_id)
    if not movie:
        return jsonify({'error': 'no such movie'}), 404
    db.session.delete(movie)

    db.session.commit()

    return jsonify({'result': 'success'}), 203
