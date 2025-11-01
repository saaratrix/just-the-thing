from flask import Flask

from .routes.embed import embed_bp
from .routes.edit import edit_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(embed_bp)
    app.register_blueprint(edit_bp)
    return app