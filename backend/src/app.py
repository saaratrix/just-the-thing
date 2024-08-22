from flask import Flask

from .routes.embed import embed_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(embed_bp)
    return app