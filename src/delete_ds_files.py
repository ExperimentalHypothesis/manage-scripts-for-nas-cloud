"""
This module is responsible for deleting all .DS_Store files in all places.
It is prerequisite for deleting empty folders.
"""
import logging
import os
from os.path import join, isfile

from constants import ROOT_FOLDER

logger = logging.getLogger(__name__)


def has_only_ds_file(folder_path: str) -> bool:
    """
    Check if folder contains DS_store file only
    """
    return os.listdir(folder_path) == [".DS_Store"]


def list_all_ds_filepaths(root_folder_path: str) -> list[str]:
    """
    Recursively find all paths to DS_store files from top to bottom.
    """
    ds = []
    for dirpath, dirnames, filenames in os.walk(root_folder_path):
        for file in filenames:
            if file.endswith(".DS_Store"):
                ds.append(join(root_folder_path, dirpath, file))
    return ds


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


def delete_all_ds_files(root_folder_path: str):
    """
    Delete all DS_store files.
    """
    files = list_all_ds_filepaths(root_folder_path)
    for file in files:
        delete_file(file)


if __name__ == "__main__":
    delete_all_ds_files(ROOT_FOLDER)