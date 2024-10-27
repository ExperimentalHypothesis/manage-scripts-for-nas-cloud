import os.path
from os.path import join

import pytest

from src.move_lossless_lossy import list_albums, move_albums, move_lossless, move_lossy, MUSIC_DIR, LOSSLESS_DIR, \
    LOSSY_DIR


@pytest.fixture
def fake_fs(fs):
    # only lossy
    fs.create_dir("/Music/B/Backworld/Isles")
    fs.create_file("/Music/B/Backworld/Isles/song1.mp3")
    fs.create_file("/Music/B/Backworld/Isles/song2.mp3")

    # only lossless
    fs.create_dir("/Music/C/Current93/Faust")
    fs.create_file("/Music/C/Current93/Faust/song1.flac")

    # mixed
    fs.create_dir("/Music/D/DO/Traces")
    fs.create_file("/Music/D/DO/Traces/song1.flac")
    fs.create_file("/Music/D/DO/Traces/song1.mp3")
    fs.create_file("/Music/D/DO/Traces/song2.flac")
    fs.create_file("/Music/D/DO/Traces/song2.mp3")


def test_list_albums_lossless(fake_fs):
    expected = ["/Music/C/Current93/Faust"]
    result = list_albums(MUSIC_DIR, lossless=True)

    assert result == expected, f"Expected {expected}, but got {result}"


def test_list_albums_lossy(fake_fs):
    expected = ["/Music/B/Backworld/Isles"]
    result = list_albums(MUSIC_DIR, lossy=True)

    assert result == expected, f"Expected {expected}, but got {result}"


def test_list_albums_lossless_and_lossy(fake_fs):
    expected = ["/Music/D/DO/Traces"]
    result = list_albums(MUSIC_DIR, lossless=True, lossy=True)

    assert result == expected, f"Expected {expected}, but got {result}"


def test_move_lossless_albums(fake_fs):
    albums = ["/Music/C/Current93/Faust"]
    move_albums(albums, lossless=True)

    assert os.path.exists("/Musick/Lossless/C/Current93/Faust/song1.flac")
    assert not os.path.exists("/Music/C/Current93/Faust/song1.flac")


def test_move_lossy_albums(fake_fs):
    albums = ["/Music/B/Backworld/Isles"]
    move_albums(albums, lossy=True)

    assert os.path.exists("/Musick/Lossy/B/Backworld/Isles/song1.mp3")
    assert os.path.exists("/Musick/Lossy/B/Backworld/Isles/song2.mp3")
    assert not os.path.exists("/Music/B/Backworld/Isles/song1.mp3")
    assert not os.path.exists("/Music/B/Backworld/Isles/song2.mp3")


def test_move_lossless(fake_fs):
    move_lossless("/Music")

    assert os.path.exists("/Musick/Lossless/C/Current93/Faust/song1.flac")
    assert not os.path.exists("/Music/C/Current93/Faust/song1.flac")


def test_move_lossy(fake_fs):
    move_lossy("/Music")

    assert os.path.exists("/Musick/Lossy/B/Backworld/Isles/song1.mp3")
    assert os.path.exists("/Musick/Lossy/B/Backworld/Isles/song2.mp3")
    assert not os.path.exists("/Music/B/Backworld/Isles/song1.mp3")
    assert not os.path.exists("/Music/B/Backworld/Isles/song2.mp3")
