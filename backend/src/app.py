from flask import Flask

from .embed.file_utility import FileUtility
from .routes.embed import embed_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(embed_bp)
    return app