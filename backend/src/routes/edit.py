import os
import re
from datetime import datetime

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from flask import Blueprint, Response, send_file, request, jsonify
from .embed import get_file_path
from ..embed.file_utility import FileUtility

edit_bp = Blueprint('edit_bp', __name__)

def create_new_filepath(file_path: str) -> str:
    timestamp = datetime.now().strftime("%m%d%H%M")

    base, ext = os.path.splitext(file_path)

    edit_part = f"_edit{timestamp}"
    if re.search(r"_edit\d{8}$", base):
        new_base = re.sub(r"_edit\d{8}$", edit_part, base)
    else:
        new_base = f"{base}{edit_part}"

    resource_url = os.path.basename(new_base)

    return f"{new_base}{ext}", edit_part, resource_url

@edit_bp.route('/edit/cut/<resource>', methods=['POST'])
def serve_file(resource: str) -> Response:
    type = request.form.get('type')
    if type != 'cut':
        return Response(status=400)

    start = request.form.get('cutStart', type=int)
    end = request.form.get('cutEnd', type=int)

    if start is None or end is None:
        return Response(status=400)

    file_path = get_file_path(resource)
    print(f"file path: {file_path} - resource: {resource}")
    if file_path is None or not os.path.exists(file_path):
        return Response(status=404)


    output, edit_part, new_resource_url = create_new_filepath(file_path)
    ffmpeg_extract_subclip(file_path, start, end, outputfile=output)

    url = f"/file/{new_resource_url}"
    media_type = FileUtility.get_media_type(output)

    return jsonify({
        "url": url,
        "mediaType": media_type,
        "resource": new_resource_url,
   })