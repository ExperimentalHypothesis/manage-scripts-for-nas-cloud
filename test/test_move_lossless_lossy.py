import os.path

import pytest

from src.move_lossless_lossy import list_albums, move_albums, move_lossless, move_lossy


@pytest.fixture
def fake_fs(fs):
    # only lossy
    fs.create_dir("/music/B/Backworld/Isles")
    fs.create_file("/music/B/Backworld/Isles/song1.mp3")
    fs.create_file("/music/B/Backworld/Isles/song2.mp3")

    # only lossless
    fs.create_dir("/music/C/Current93/Faust")
    fs.create_file("/music/C/Current93/Faust/song1.flac")

    # mixed
    fs.create_dir("/music/D/DO/Traces")
    fs.create_file("/music/D/DO/Traces/song1.flac")
    fs.create_file("/music/D/DO/Traces/song1.mp3")
    fs.create_file("/music/D/DO/Traces/song2.flac")
    fs.create_file("/music/D/DO/Traces/song2.mp3")


def test_list_albums_lossless(fake_fs):
    expected = ["/music/C/Current93/Faust"]
    result = list_albums("/music", lossless=True)

    assert result == expected, f"Expected {expected}, but got {result}"


def test_list_albums_lossy(fake_fs):
    expected = ["/music/B/Backworld/Isles"]
    result = list_albums("/music", lossy=True)

    assert result == expected, f"Expected {expected}, but got {result}"


def test_list_albums_lossless_and_lossy(fake_fs):
    expected = ["/music/D/DO/Traces"]
    result = list_albums("/music", lossless=True, lossy=True)

    assert result == expected, f"Expected {expected}, but got {result}"


def test_move_lossless_albums(fake_fs):
    albums = ["/music/C/Current93/Faust"]
    move_albums(albums, lossless=True)

    assert os.path.exists("/musick/lossless/C/Current93/Faust/song1.flac")
    assert not os.path.exists("/music/C/Current93/Faust/song1.flac")


def test_move_lossy_albums(fake_fs):
    albums = ["/music/B/Backworld/Isles"]
    move_albums(albums, lossy=True)

    assert os.path.exists("/musick/lossy/B/Backworld/Isles/song1.mp3")
    assert os.path.exists("/musick/lossy/B/Backworld/Isles/song2.mp3")
    assert not os.path.exists("/music/B/Backworld/Isles/song1.mp3")
    assert not os.path.exists("/music/B/Backworld/Isles/song2.mp3")


def test_move_lossless(fake_fs):
    move_lossless("/music")

    assert os.path.exists("/musick/lossless/C/Current93/Faust/song1.flac")
    assert not os.path.exists("/music/C/Current93/Faust/song1.flac")


def test_move_lossy(fake_fs):
    move_lossy("/music")

    assert os.path.exists("/musick/lossy/B/Backworld/Isles/song1.mp3")
    assert os.path.exists("/musick/lossy/B/Backworld/Isles/song2.mp3")
    assert not os.path.exists("/music/B/Backworld/Isles/song1.mp3")
    assert not os.path.exists("/music/B/Backworld/Isles/song2.mp3")
