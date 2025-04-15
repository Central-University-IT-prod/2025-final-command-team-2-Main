from flask import Blueprint, jsonify
from app.helpers import check_token

users_bp = Blueprint('users', __name__)

@users_bp.route('/me')
@check_token
def me(user):
    return jsonify(user.to_dict())
