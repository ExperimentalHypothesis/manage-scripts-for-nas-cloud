"""
This module is responsible for deleting folders where no audio files are present.
It can be folders with some log, pictures, cue files and other crap.
The point is that if no audio is present, keeping such folder is useless.
"""

import os
from os.path import join

from src.exceptions import AudioFileDeleteErr

LOSSY_ENCODINGS = {"mp3", "mp4", "ogg", "m4a"}
LOSSLESS_ENCODINGS = {"flac", "ape", "wma"}
AUDIO_EXTENSIONS = LOSSY_ENCODINGS | LOSSLESS_ENCODINGS


def get_all_extensions(root_folder_path: str) -> set[str]:
    """
    Get all extensions from all files in given directory.
    """
    extensions = set()
    for dirpath, dirnames, filenames in os.walk(root_folder_path):
        for file in filenames:
            ext = file.split(".")[-1]
            extensions.add(ext)

    return extensions


def list_folders_with_no_audio_files(root_folder_path: str) -> list[str]:
    """
    List folders where no audio files are located - such folders should be deleted.
    """
    folders = []
    for dirpath, dirnames, filenames in os.walk(root_folder_path, topdown=False):
        if not filenames:
            continue
        if all(not file.endswith(tuple(AUDIO_EXTENSIONS)) for file in os.listdir(dirpath)):
            folders.append(dirpath)

    return folders


def delete_files_in_folder(folder_path: str):
    """
    Delete all files in folder.
    The files should be NON audio files, if there is an audiofile it is a mistake -> throw.
    """
    for file in os.listdir(folder_path):
        if file.endswith(tuple(AUDIO_EXTENSIONS)):
            raise AudioFileDeleteErr(f"File {file} is audio")

        os.remove(join(folder_path, file))
        print(f"Deleted {join(folder_path, file)}")


def delete_folders_with_no_audio_files(root_folder_path: str):
    """
    Delete all folders with no audio files.
    """
    folders = list_folders_with_no_audio_files(root_folder_path)
    for folder in folders:
        try:
            delete_files_in_folder(folder)
            os.rmdir(folder)
        except AudioFileDeleteErr as err:
            print(err)
        except OSError as err:
            print(err)


if __name__ == "__main__":
    # ROOT_FOLDER = "/Users/lukas.kotatko/TESTING_FILESYSTEM"
    ROOT_FOLDER = "/shares/Public/Music"

    delete_folders_with_no_audio_files(ROOT_FOLDER)
