import os.path
from flask import Blueprint, Response, after_this_request, current_app, send_file

from backend.src.embed.embed_types import get_embedder

embed_bp = Blueprint('embed_bp', __name__)


@embed_bp.route('/embed/<path:url>', methods=['GET'])
def embed(url: str) -> tuple[str, int] | Response:
    print(url)
    # find out the kind of checks we want to do based on the <url>
    embedder = get_embedder(url)
    if embedder is None:
        return Response(status=404)

    resource_path = embedder.fetch_embed_resource(url)
    if not resource_path:
        return Response(status=404)

    @after_this_request
    def remove_file(response):
        try:
            if os.path.exists(resource_path):
                os.remove(resource_path)
        except OSError as e:
            current_app.logger.error("Error removing file: %s - %s", resource_path, e)
        return response

    return send_file(resource_path, as_attachment=True)
