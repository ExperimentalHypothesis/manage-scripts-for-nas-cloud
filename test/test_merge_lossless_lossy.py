import pytest

from src.merge_lossy_lossless import LOSSLESS_DIR, LOSSY_DIR


@pytest.fixture
def fake_fs(fs):
    # lossy
    fs.create_dir("/Music/Lossless/B/Backworld/Isles")


    # lossless
    fs.create_dir("/Music/B/Backworld/Isles")
    fs.create_file("/Music/B/Backworld/Isles/song1.mp3")
    fs.create_file("/Music/B/Backworld/Isles/song2.mp3")
