import os
from flask import Flask
from flask_cors import CORS

from src.database import db
from src.notes import notes


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.app = app
    db.init_app(app)

    app.register_blueprint(notes)

    @app.errorhandler(404)
    def handle_404(e):
        return {"error": "Not found"}, 404

    @app.errorhandler(500)
    def handle_500(e):
        return {"error": "Something went wrong. Please try again."}, 500

    return app
