import mimetypes
import os


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
