import mimetypes
import os
from .temp_folder_handler import TempFolderHelper

class FileUtility:
    SUPPORTED_MEDIA_TYPES = {
        ".mp4": "video/mp4",
    }

    @staticmethod
    def get_media_type(file_path: str) -> str | None:
        _, file_extension = os.path.splitext(file_path)

        media_type = FileUtility.SUPPORTED_MEDIA_TYPES.get(file_extension.lower())

        if media_type is None:
            return None

        return media_type

    @staticmethod
    def try_get_file_from_url(url: str) -> (str | None, str | None):
        contains, path = TempFolderHelper.contains_file(url)
        if contains:
            return url, FileUtility.get_media_type(url)

        extensions = FileUtility.SUPPORTED_MEDIA_TYPES.keys()
        for extension in extensions:
            file = url + extension
            contains, path =  TempFolderHelper.contains_file(file)
            if contains:
                media_type = FileUtility.SUPPORTED_MEDIA_TYPES[extension]
                return file, media_type

        return None, None