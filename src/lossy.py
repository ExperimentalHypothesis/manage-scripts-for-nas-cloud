import os
from os.path import join, isdir, isfile

ROOT_FOLDER = "/Users/lukas.kotatko/TESTING_FILESYSTEM"


class Lossy:
    encodings = {"mp3"}

    @staticmethod
    def list_all_albums(folder_path: str) -> list[str]:
        albums = []
        for letter in os.listdir(folder_path):
            letter_path = join(folder_path, letter)
            if isfile(letter_path):
                continue

            for artist in os.listdir(join(folder_path, letter)):
                artist_path = join(letter_path, artist)
                if isfile(artist_path):
                    continue

                for album in os.listdir(artist_path):
                    album_path = join(artist_path, album)
                    if isfile(album_path):
                        continue

                    if any(song.endswith(tuple(Lossy.encodings)) for song in os.listdir(album_path)):
                        albums.append(album_path)
        return albums





if __name__ == "__main__":
    print(Lossy.list_all_albums(ROOT_FOLDER))


