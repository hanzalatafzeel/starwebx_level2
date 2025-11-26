import os
from datetime import timedelta

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///invoicegen.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # CORS (safe parser)
    _raw_origins = os.getenv('CORS_ORIGINS', 'http://localhost:5173' ,'https://starwebx-level2.vercel.app')
    if _raw_origins.strip() == "*" or _raw_origins.strip().lower() == "all":
        CORS_ORIGINS = "*"
    else:
        CORS_ORIGINS = [o.strip() for o in _raw_origins.split(",") if o.strip()]
