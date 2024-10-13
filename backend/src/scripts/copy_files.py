import argparse
import glob
import os
import shutil
from typing import List, Tuple

TARGET_DIRECTORY = ""
ROOT_PATH = ""


# Copied from file_manager ensure_directory_exists()
def ensure_directory_exists(file_path: str) -> None:
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory, 0o777, True)


def copy_file(source: str, target: str, only_print_errors: bool) -> bool:
    source_abs = os.path.abspath(source)
    target_abs = os.path.abspath(target)

    if not os.path.exists(source):
        print(f"\033[91mCould not copy {source} as it does not exist.[0m")
        return False

    if not only_print_errors:
        print(f"Copied {source} to {target}")

    try:
        ensure_directory_exists(target_abs)
        shutil.copy2(source_abs, target_abs)
        return True
    except Exception as e:
        print(f"\033[91mFailed to copy file {source} because {e}\033[0;0m")
        return False


def copy_all_files(include_pattern: str, exclude_patterns: List[str], only_print_errors: bool) -> Tuple[int, int]:
    files = glob.glob(include_pattern, recursive=True)
    successes = 0
    fails = 0

    for file in files:
        if not can_copy_file(file, exclude_patterns):
            continue

        relative_path = file.replace(ROOT_PATH, "")
        target_file = os.path.join(TARGET_DIRECTORY, relative_path)
        if copy_file(file, target_file, only_print_errors):
            successes += 1
        else:
            fails += 1

    return successes, fails


def can_copy_file(path, exclude_patterns) -> bool:
    for pattern in exclude_patterns:
        if pattern in path:
            return False

    return True


"""
Copies the server files from this project.
"""
def main():
    parser = argparse.ArgumentParser(description="Move server files from this project to target destination.")
    parser.add_argument("--target", required=True, help="Target directory for moving files.")
    # Add the "--venv" argument (not required with a default value)
    parser.add_argument("--venv", default="env", help="Python's venv folder path")
    args = parser.parse_args()

    global TARGET_DIRECTORY
    global ROOT_PATH

    TARGET_DIRECTORY = args.target
    current_file = os.path.dirname(os.path.abspath(__file__))
    # ".." from scripts --> src
    # ".." from src --> server
    ROOT_PATH = os.path.abspath(os.path.join(current_file, "..", "..", ""))
    # Check if the last character of root_path is not a slash or backslash
    if not ROOT_PATH.endswith(os.path.sep):
        ROOT_PATH = os.path.join(ROOT_PATH, "")

    files_to_move = [
        "wsgi.py",
        "requirements.txt"
    ]

    folder_searches = [
        {"includes": ["src/**/*.py"], "excludes": ["tests"], "only_print_errors": False},
        {"includes": ["src/**/*.html"], "excludes": ["tests"], "only_print_errors": False},
        {"includes": ["src/**/*.css"], "excludes": ["tests"], "only_print_errors": False},
        {"includes": ["src/**/*.js"], "excludes": ["tests"], "only_print_errors": False},
    ]

    successes = 0
    fails = 0

    for file_to_move in files_to_move:
        path = os.path.join(ROOT_PATH, file_to_move)
        target = os.path.join(TARGET_DIRECTORY, file_to_move)
        if copy_file(path, target, False):
            successes += 1
        else:
            fails += 1

    for folder_search in folder_searches:
        for include_pattern in folder_search["includes"]:
            # Need to include the path or the glob doesn't work.
            include_pattern = os.path.join(ROOT_PATH, include_pattern)
            result = copy_all_files(include_pattern, folder_search["excludes"], folder_search["only_print_errors"])
            successes += result[0]
            fails += result[1]

    print("Finished copy all files.")
    print(f"Succesfully copied {successes} and failed to copy {fails}")

# Test script:
# python src\scripts\copy_files.py --target temp\scripts
if __name__ == "__main__":
    main()
