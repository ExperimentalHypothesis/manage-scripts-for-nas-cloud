"""
This module is used to create a new structure for the audio files.
There will one new root folder Musick and it will contain two subfolders - lossless and lossy.
Inside these tow will be alphabetical structure as usual.
"""

import os
import shutil
from contextlib import contextmanager
from os.path import join, isfile

LOSSY_ENCODINGS = {"mp3", "mp4", "ogg", "m4a"}
LOSSLESS_ENCODINGS = {"flac", "ape", "wma"}
MUSIC_DIR = "/Music"
LOSSLESS_DIR = "/Musick/Lossless"
LOSSY_DIR = "/Musick/Lossy"



def list_albums(folder_path: str, lossless: bool = False, lossy: bool = False) -> list[str]:
    """
    List albums based on given params.
    Either albums with lossless audio.
    Or albums with lossy audio.
    Or albums with both lossless and lossy - should not happen as it is a mistake of a kind.
    """

    albums = []

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

                songs = os.listdir(album_path)

                has_lossless = any(song.casefold().endswith(tuple(LOSSLESS_ENCODINGS)) for song in songs)
                has_lossy = any(song.casefold().endswith(tuple(LOSSY_ENCODINGS)) for song in songs)

                if lossless and lossy:
                    if has_lossless and has_lossy:
                        albums.append(album_path)
                elif lossless:
                    if has_lossless and not has_lossy:
                        albums.append(album_path)
                elif lossy:
                    if has_lossy and not has_lossless:
                        albums.append(album_path)

    return albums


def move_albums(albums: list[str], lossless: bool = False, lossy: bool = False):
    """
    Moves album folders to new location
    """
    if lossless and lossy:
        raise RuntimeError("Either lossless or lossy can be specified but not both")

    for src in albums:
        dst = src.replace(MUSIC_DIR, LOSSLESS_DIR) if lossless else src.replace(MUSIC_DIR, LOSSY_DIR)
        shutil.move(src, dst)
        print(f"moved {src} to {dst}")


@contextmanager
def encoding(lossless=False, lossy=False):
    """
    Set the encoding.
    Instead of passing the same arg into multiple function calls. Use this.
    """
    if not lossless and not lossy:
        raise RuntimeError("Either lossless or lossy has to be specified")

    config = {
        "lossless": lossless,
        "lossy": lossy
    }

    yield config


def move_lossless(folder_path: str):
    """ Entry point for moving lossless """
    with encoding(lossless=True) as config:
        lossless_albums = list_albums(folder_path, **config)
        move_albums(lossless_albums, **config)


def move_lossy(folder_path: str):
    """ Entry point for moving lossy """
    with encoding(lossy=True) as config:
        lossy_albums = list_albums(folder_path, **config)
        move_albums(lossy_albums, **config)


if __name__ == "__main__":
    ROOT_FOLDER = "/Users/lukas.kotatko/TESTING_FILESYSTEM"
    list_albums(ROOT_FOLDER, lossless=True, lossy=True)
