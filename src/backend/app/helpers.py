from functools import wraps
from app.models import User
from flask import jsonify, request, current_app
import jwt
from datetime import datetime, UTC


def check_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')

        if not token:
            return jsonify({
                'code': 401,
                'message': 'Missing token'
            }), 401

        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        except Exception as e:
            return jsonify({
                'code': 401,
                'message': 'Invalid token'
            }), 401

        user_id = payload.get('user_id')
        telegram_id = payload.get('telegram_id')
        exp = payload.get('exp')

        if not user_id or not exp or not telegram_id:
            return jsonify({
                'code': 401,
                'message': 'Invalid token'
            }), 401

        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({
                'code': 404,
                'message': 'User not found'
            }), 404

        current_timestamp = datetime.now(UTC).timestamp()
        if exp < current_timestamp:
            return jsonify({
                'code': 401,
                'message': 'Token expired'
            }), 401

        return func(user, *args, **kwargs)

    return wrapper