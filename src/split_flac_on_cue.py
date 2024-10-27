"""
This module is used for slipping one flac file into many based on cue file.
The original flac will be deleted, as well as the original cue.

"""

import os
from os.path import join, isfile

CUE = ".cue"
FLAC = ".flac"

def has_one_cue_for_one_flac(album_path: str) -> bool:
    """
    Check if the album has cue file and flac file associated with it
    """
    flac_files = 0
    cue_files = 0
    for file in os.listdir(album_path):
        if file.endswith(FLAC):
            flac_files += 1
        if file.endswith(CUE):
            cue_files += 1

    return flac_files == 1 and cue_files == 1


def get_cue_pathfile(album_path: str) -> str:
    """
    Get the path of the cue file used for splitting
    """
    for file in os.listdir(album_path):
        if file.endswith(CUE):
            return join(album_path, file)


def list_cue_files(folder_path: str):
    """
    List all cue files which will split flac
    """
    cues = []
    for letter in os.listdir(folder_path):
        letter_path = join(folder_path, letter)
        if isfile(letter_path):
            continue

        for artist in os.listdir(letter_path):
            artist_path = join(letter_path, artist)
            if isfile(artist_path):
                continue

            for album in os.listdir(artist_path):
                album_path = join(artist_path, album)
                if isfile(album_path):
                    continue

                if has_one_cue_for_one_flac(album_path):
                    cues.append(get_cue_pathfile(album_path))

    return cues




