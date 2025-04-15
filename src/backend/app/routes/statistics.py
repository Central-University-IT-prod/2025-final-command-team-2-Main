from flask import Blueprint, jsonify
from app.helpers import check_token
from app.models import User, Movie, CollectionUser, Collection
from app import db

bp = Blueprint('statistic_bp', __name__)


@bp.route('/added_movies', methods=['GET'])
@check_token
def get_added_movies(user: User):
    user_collections: list[CollectionUser] = CollectionUser.query.filter_by(telegram_id=user.telegramId).all()
    collections = [db.session.get(Collection, col.collection_id) for col in user_collections]
    result = 0
    for col in collections:
        result += len(col.movies)


    return jsonify({'user_id': user.telegramId, 'added_movies': result})

