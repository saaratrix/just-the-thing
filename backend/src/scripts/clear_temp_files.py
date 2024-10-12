import os
import time

from backend.src.embed.temp_folder_handler import TempFolderHelper


def clear_old_temp_files(max_age_seconds: int = 60 * 60 * 24):
    """Clears files older than max_age_seconds in the given folder."""
    current_time = time.time()
    folder_path = TempFolderHelper.get_temp_folder_path()

    if not os.path.exists(folder_path):
        print(f"Folder path does not exist: {folder_path}")
        return

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > max_age_seconds:
                os.remove(file_path)
                print(f"Removed {file_path} (age: {file_age} seconds)")

if __name__ == "__main__":
    clear_old_temp_files()