from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config
from flask_swagger_ui import get_swaggerui_blueprint

db = SQLAlchemy()
migrate = Migrate(render_as_batch=True)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(app, resources={r"/*": {"origins": "*"}})

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import User
    from app.models import Movie
    from app.models import Collection
    from app.models import CollectionUser

    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.search import search_bp
    from app.routes.users import users_bp
    from app.routes.movie import movie_bp
    from app.routes.collections import collection_bp
    
    SWAGGER_URL = '/api/docs'
    API_URL = '/api/static/openapi.yaml'
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Фильм на вечер API"
        }
    )
    
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    app.register_blueprint(main_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(search_bp, url_prefix='/api/movie/search')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(movie_bp, url_prefix='/api/movies')
    app.register_blueprint(collection_bp, url_prefix='/api/collections')

    return app
