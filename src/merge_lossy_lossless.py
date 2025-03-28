import shutil
import os
from string import ascii_uppercase


LOSSLESS_DIR = "/shares/Public/Musick/Lossless"
LOSSY_DIR = "/shares/Public/Musick/Lossy"

def merge_lossless_lossy(root): # root = A
    for artist in os.listdir(root):
        lossy_artist_path = os.path.join(root, artist)
        lossless_artist_path = lossy_artist_path.replace(LOSSY_DIR, LOSSLESS_DIR)
        if os.path.exists(lossless_artist_path):
            print(f"Artists EXISTS on path {lossless_artist_path} -- checking its albums..")
            for album in os.listdir(lossy_artist_path):
                lossy_album_path = os.path.join(lossy_artist_path, album)
                lossless_album_path = os.path.join(lossless_artist_path, album)

                if os.path.exists(lossless_album_path):
                    print(f"\tAlbum EXISTS on path {lossless_album_path} -- skipping it..")
                    continue

                else:
                    print(f"\tAlbum NOT EXIST on path {lossless_album_path} --  moving it..")
                    shutil.move(lossy_album_path, lossless_artist_path)
        else:
            print(f"Artists NOT EXISTS on path {lossless_artist_path} -- moving it..")
            shutil.move(lossy_artist_path, lossless_artist_path)


if __name__ == "__main__":
    for letter in ascii_uppercase:
        root = os.path.join(LOSSY_DIR, letter)
        merge_lossless_lossy(root)
