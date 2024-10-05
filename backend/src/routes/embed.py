import os.path
from flask import Blueprint, Response, after_this_request, current_app, send_file, render_template, jsonify

from backend.src.embed.embed_types import get_embedder
from backend.src.embed.file_utility import FileUtility
from backend.src.embed.temp_folder_handler import TempFolderHelper

embed_bp = Blueprint('embed_bp', __name__)

@embed_bp.route('/embed', methods=['GET'])
def index() -> Response:
    return render_template('embed.html')

@embed_bp.route('/download/<path:url>', methods=['GET'])
def embed(url: str) -> tuple[str, int] | Response:
    print(url)
    # find out the kind of checks we want to do based on the <url>
    embedder = get_embedder(url)
    if embedder is None:
        return Response(status=404)

    resource_path = embedder.fetch_embed_resource(url)
    if not resource_path:
        return Response(status=404)

    return send_file(resource_path, as_attachment=True)


def get_file_path(resource_name: str) -> str:
    folder_path = TempFolderHelper.get_temp_folder_path()
    file_path = os.path.join(folder_path, resource_name)
    return file_path

@embed_bp.route('/file/<filename>', methods=['GET'])
def serve_file(filename: str) -> Response:
    file_path = get_file_path(filename)

    if not os.path.exists(file_path):
        return Response(status=404)

    return send_file(file_path)

def get_embed_resource_url(url: str) -> str | None:
    embedder = get_embedder(url)
    if embedder is None:
        return Response(status=404)

    resource_path = embedder.fetch_embed_resource(url)
    if not resource_path:
        return Response(status=404)

    resource_filename = os.path.basename(resource_path)
    media_type = FileUtility.get_media_type(resource_filename)
    return f"/file/{resource_filename}", media_type

@embed_bp.route('/embed/file/<path:url>', methods=['GET'])
def get_resource_url(url: str) -> tuple[str, int] | Response:
    resource_filename, media_type = get_embed_resource_url(url)
    return jsonify({
        "url": resource_filename,
        "mediaType": media_type
   })

@embed_bp.route('/embed/view/<path:url>', methods=['GET'])
def view(url: str) -> tuple[str, int] | Response:
    resource_url, media_type = get_embed_resource_url(url)

    return render_template('embed_video.html', resource_url=resource_url, resource_type=media_type)
