import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:postgres@localhost:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PORT = int(os.environ.get('PORT', 8080))
    HOST = os.environ.get('HOST', 'localhost')
    
    # JWT Settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or '123123'
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24 * 30 # 30 дней