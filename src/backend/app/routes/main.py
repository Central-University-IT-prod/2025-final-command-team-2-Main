import os
from dotenv import load_dotenv

from flask import Blueprint, jsonify, request, send_from_directory, current_app, send_file
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return jsonify({'123': '123'})

@main_bp.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@main_bp.route('/clear_tables', methods=['DELETE'])
def clear_table():
    load_dotenv()
    password = request.headers.get('Password')
    if password != os.environ.get('BD_PASS'):
        return jsonify({'error': 'you have no access to this page'}), 403
    tables = request.args.getlist('tables')
    print(tables)
    for table_name, table in db.metadata.tables.items():
        print(table_name)
        if table_name in tables[0]:
            db.session.execute(table.delete())
    db.session.commit()
    return jsonify({'ok': '1'}), 200

@main_bp.route('/test_coverage', methods=['GET'])
def test_coverage():
    return send_file('../htmlcov/index.html')