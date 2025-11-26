# app.py
import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config
from models import db
import controllers  # blueprint import here

load_dotenv()  # load .env in development

def _normalize_origins(origins):
    """
    Accepts Config.CORS_ORIGINS which may be:
      - "*" (string) -> returns "*"
      - "http://a.com" (string) -> returns "http://a.com"
      - ["http://a.com","http://b.com"] (list) -> returns list
    Returns a value acceptable by flask_cors.CORS
    """
    if origins is None:
        return "*"
    # If already wildcard
    if isinstance(origins, str) and origins.strip() == "*":
        return "*"
    # If list-like, return list (ensuring strings)
    if isinstance(origins, (list, tuple)):
        return [str(o).strip() for o in origins if str(o).strip()]
    # otherwise, return trimmed string
    return str(origins).strip()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # init extensions
    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    # Normalize CORS origins from Config
    origins = _normalize_origins(app.config.get("CORS_ORIGINS", "*"))

    # Configure CORS:
    # - apply CORS to API and uploads routes
    # - allow default methods
    # - do not enable credentials by default (enable if you use cookie-based auth)
    CORS(app, resources={
        r"/api/*": {"origins": origins},
        r"/uploads/*": {"origins": origins}
    })

    # register routes/blueprints
    app.register_blueprint(controllers.bp, url_prefix="/api")

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    return app

# WSGI entrypoint for gunicorn
app = create_app()

if __name__ == "__main__":
    # create DB only in dev if wanted
    if os.environ.get("FLASK_ENV") == "development" or os.environ.get("CREATE_DB_ON_START", "false").lower() == "true":
        with app.app_context():
            db.create_all()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=(os.environ.get("FLASK_ENV") == "development"))
