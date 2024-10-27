import os
from collections import defaultdict
import hashlib
import logging

logger = logging.getLogger(__name__)

ROOT_FOLDER = "/Users/lukas.kotatko/TESTING_FILESYSTEM"
# ROOT_FOLDER = "/shares/Public/Music"


def get_files_with_same_size(root_folder: str) -> dict[int, list[str]]:
    """Find files that have the same size and return them as a dict where key is size and value is list of filepaths."""
    d = defaultdict(list)
    for dirpath, _, files in os.walk(root_folder):
        for file in files:
            filepath = os.path.join(dirpath, file)
            filesize = os.path.getsize(filepath)
            d[filesize].append(filepath)

    return {size: paths for size, paths in d.items() if len(paths) > 1}


def calculate_hash(filepath: str) -> str:
    """Generate a hash for the file using SHA-256."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            hasher.update(chunk)

    return hasher.hexdigest()


def get_files_with_same_hash(filepaths: list[str]) -> dict[str, list[str]]:
    """ Given list of filepaths, calculate hash for each file. """
    d = defaultdict(list)
    for file in filepaths:
        logger.warning(f"Calculating hash for file {file}")
        hash = calculate_hash(file)
        logger.warning(f"Hash for file {file} is {hash}")
        d[hash].append(file)
    return {hash: files for hash, files in d.items() if len(files) > 1}


def find_duplicates(root_folder_path: str):
    """ Find duplicated files and store them in a file. """
    size_files_map = get_files_with_same_size(root_folder_path)
    with open("files_hashes.txt", "w") as f:
        for size, files in size_files_map.items():
            f.write(f"size: {size}\n \thash {get_files_with_same_hash(files)}\n")



if __name__ == "__main__":
    find_duplicates(ROOT_FOLDER)