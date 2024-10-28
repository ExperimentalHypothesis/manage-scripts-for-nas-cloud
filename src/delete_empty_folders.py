"""
This module is responsible for deleting empty folders.
It should be run after 'delete_ds_files' module.
The final state should be such that only folders with audio files are present.
"""


import os
import logging
from os.path import join, dirname, isfile

logger = logging.getLogger(__name__)

ROOT_FOLDER = "/Users/lukas.kotatko/TESTING_FILESYSTEM"


def is_folder_empty(folder_path: str):
    """
    Check if folder is empty.
    """
    return not os.listdir(folder_path)


def list_all_empty_folders(root_folder_path: str):
    """
    Recursively find all empty folders from top to bottom.
    """
    paths = []
    for path in os.listdir(root_folder_path):
        full_path = join(root_folder_path, path)
        if isfile(full_path):
            continue

        if is_folder_empty(full_path):
            paths.append(full_path)
        else:
            paths.extend(list_all_empty_folders(full_path))
    return paths


def delete_folder(folder_path: str):
    """
    Delete folder on given path.
    """
    try:
        os.rmdir(folder_path)
        logger.warning(f"Deleted folder on path {folder_path}")
    except OSError as e:
        logger.exception("Could not delete folder on path %s due to err %s", folder_path, e)


def delete_empty_folders(root_folder_path: str):
    """
    Recursively delete all empty folders from bottom to up.
    """
    empty_folders = list_all_empty_folders(root_folder_path)
    for empty_folder in empty_folders:
        delete_folder(empty_folder)

        parent_folder = dirname(empty_folder)

        while parent_folder and parent_folder != root_folder_path:
            if is_folder_empty(parent_folder):
                delete_folder(parent_folder)
                parent_folder = dirname(parent_folder)
            else:
                break


if __name__ == "__main__":
    delete_empty_folders(ROOT_FOLDER)
