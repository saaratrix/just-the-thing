import os
import time
from typing import List


class TempFolderHelper:
    _temp_folder_path = None
    _temp_folder_name = 'temp_files'

    ROOT_PATH = None

    @staticmethod
    def get_app_root_path():
        if TempFolderHelper.ROOT_PATH is not None:
            return TempFolderHelper.ROOT_PATH

        current_file_path = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_file_path)
        path = os.path.join(current_dir, "..", "..")
        TempFolderHelper.ROOT_PATH = os.path.normpath(os.path.abspath(path))
        return TempFolderHelper.ROOT_PATH

    @staticmethod
    def get_temp_folder_path():
        if TempFolderHelper._temp_folder_path is not None:
            return TempFolderHelper._temp_folder_path

        root_path = TempFolderHelper.get_app_root_path()
        path = os.path.join(root_path, TempFolderHelper._temp_folder_name)
        TempFolderHelper._temp_folder_path = os.path.normpath(os.path.abspath(path))
        TempFolderHelper.ensure_directory()
        return TempFolderHelper._temp_folder_path

    @staticmethod
    def contains_file(file_name) -> tuple[bool, None] | tuple[bool, str]:
        temp_folder = TempFolderHelper.get_temp_folder_path()
        path = os.path.normpath(os.path.join(temp_folder, file_name))

        if not path.startswith(temp_folder):
            return False, None

        return os.path.exists(path), path

    @staticmethod
    def get_temp_folder_files():
        return os.listdir(TempFolderHelper.get_temp_folder_path())

    @staticmethod
    def get_new_temp_folder_files(old_files):
        new_files = []
        for file in TempFolderHelper.get_temp_folder_files():
            if file not in old_files:
                new_files.append(file)
        return new_files

    @staticmethod
    def ensure_directory():
        path = TempFolderHelper._temp_folder_path
        if path is None or os.path.exists(path):
            return

        os.makedirs(path)
        # Grants read and write permissions to the owner
        os.chmod(path, 0o600)

    @staticmethod
    def try_remove_old_files(hours: int, ignore: str | None):
        try:
            cutoff = time.time() - (hours * 3600)
            to_delete: List[str] = []
            temp_folder = TempFolderHelper.get_temp_folder_path()
            for file in TempFolderHelper.get_temp_folder_files():
                if ignore is not None and file.startswith(ignore.lower()):
                    continue

                path = os.path.join(temp_folder, file)

                if os.path.getmtime(path) < cutoff:
                    to_delete.append(path)

            for file in to_delete:
                print(f"Removed file {file}")
                os.remove(file)
        except Exception as e:
            print(f"Failed to remove old files: {e}")


