import os
from os.path import join, isdir, isfile

ROOT_FOLDER = "/Users/lukas.kotatko/TESTING_FILESYSTEM"

LOSSY_ENCODINGS = {"mp3"}
LOSSLESS_ENCODINGS = {"flac"}


def list_albums(folder_path: str, lossless: bool = False, lossy: bool = False) -> list[str]:
    """
    List albums based on given params.
    Either albums with lossless audio.
    Or albums with lossy audio.
    Or albums with both lossless and lossy - should not happens as it is a mistake of a kind.
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


