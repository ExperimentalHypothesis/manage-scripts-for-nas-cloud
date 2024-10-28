"""
This module is responsible for deleting all .DS_Store files in all places.
It is prerequisite for deleting empty folders.
"""
import logging
import os
from os.path import join, isfile

logger = logging.getLogger(__name__)


def has_only_ds_file(folder_path: str) -> bool:
    """
    Check if folder contains DS_store file only
    """
    return os.listdir(folder_path) == [".DS_Store"]


def list_all_ds_filepaths(root_folder_path: str):
    """
    Recursively find all paths to DS_store files from top to bottom.
    """
    paths = []
    for path in os.listdir(root_folder_path):
        full_path = join(root_folder_path, path)
        if isfile(full_path):
            continue

        if has_only_ds_file(full_path):
            paths.append(join(full_path, ".DS_Store"))
        else:
            paths.extend(list_all_ds_filepaths(full_path))
    return paths


def delete_file(file_path: str):
    """
    Delete DS_store file on given path.
    """
    if not file_path.endswith(".DS_Store"):
        raise RuntimeError(f"Filepath {file_path} does not contain DS_Store file")

    try:
        os.remove(file_path)
        logger.warning(f"Deleted file on path {file_path}")
    except OSError as e:
        logger.exception("Could not delete file on path %s due to err %s", file_path, e)

