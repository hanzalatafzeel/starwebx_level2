from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from config import Config
from models import db
import controllers  # yahan se blueprint import hoga

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app, origins=app.config.get('CORS_ORIGINS', '*'))

# ✅ Register all routes from controllers
app.register_blueprint(controllers.bp, url_prefix="/api")


# CLI command to initialize database
@app.cli.command()
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()
    print('✅ Database initialized!')


# Run application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
