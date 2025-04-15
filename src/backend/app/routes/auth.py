from flask import Blueprint, jsonify, request, current_app
from app.models import User
from app import db
from pydantic import BaseModel, Field
import jwt
from datetime import datetime, timedelta, UTC
from app.models import Collection, CollectionUser

auth_bp = Blueprint('auth', __name__)

class TelegramAuthRequest(BaseModel):
    telegramId: int
    username: str 
    avatarUrl: str = ''

def generate_token(user_id: int, telegram_id: int) -> str:
    payload = {
        'user_id': user_id,
        'telegram_id': telegram_id,
        'exp': datetime.now(UTC) + timedelta(seconds=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

@auth_bp.route('/telegram', methods=['POST'])
def telegram_auth():
    data = request.get_json()
    
    try:
        if isinstance(data.get('telegramId'), str):
            data['telegramId'] = int(data['telegramId'])
        auth_data = TelegramAuthRequest(**data)
    except ValueError as e:
        return jsonify({
            'code': 400,
            'message': 'Invalid telegram ID format',
            'details': {
                'errors': str(e)
            }
        }), 400
    except Exception as e:
        return jsonify({
            'code': 400,
            'message': 'Missing required fields',
            'details': {
                'errors': str(e)
            }
        }), 400

    user = User.query.filter_by(telegramId=auth_data.telegramId).first()
    is_new_user = user is None

    if is_new_user:
        user = User(
            telegramId=auth_data.telegramId,
            username=auth_data.username,
            avatarUrl=auth_data.avatarUrl
        )
        collection = Collection()
        collection.name = 'Ваши фильмы'
        collection.description = 'Это ваши сохраненные фильмы'
        collection.is_default = True
        db.session.add(user)
        db.session.add(collection)
        db.session.commit()

        user_collection = CollectionUser()
        user_collection.collection_id = collection.id
        print(collection.id)
        user_collection.telegram_id = user.telegramId

        db.session.add(user_collection)

    else:
        user.username = auth_data.username
        user.avatarUrl = auth_data.avatarUrl

    db.session.commit()

    # Generate JWT token
    token = generate_token(user.id, user.telegramId)

    return jsonify({
        'user': user.to_dict(),
        'isNewUser': is_new_user,
        'token': token
    })
