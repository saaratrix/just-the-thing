import os


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
    def contains_file(file_name) -> bool:
        temp_folder = TempFolderHelper.get_temp_folder_path()
        path = os.path.join(temp_folder, file_name)
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