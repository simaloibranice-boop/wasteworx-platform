from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

from .extensions import db, jwt


def create_app():
    load_dotenv()

    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    CORS(app)

    db.init_app(app)
    jwt.init_app(app)

    from . import models
    from .api.auth.routes import auth_bp

    app.register_blueprint(auth_bp)

    @app.get("/api/health")
    def health_check():
        return {
            "status": "ok",
            "message": "Wasteworx API is running"
        }

    return app
