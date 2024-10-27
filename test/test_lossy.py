import os

import pytest

from src.lossy import Lossy


@pytest.fixture
def fake_fs(fs):
    fs.create_dir("/music/A/Alio Die/Apsaras")
    fs.create_file("/music/A/Alio Die/Apsaras/song1.mp3")
    fs.create_file("/music/A/Alio Die/Apsaras/song2.mp3")
    fs.create_file("/music/A/Alio Die/Apsaras/song3.mp3")

    fs.create_dir("/music/B/Backworld/Isles")
    fs.create_file("/music/B/Backworld/Isles/song1.mp3")
    fs.create_file("/music/B/Backworld/Isles/song2.mp3")

    fs.create_dir("/music/C/Current93/Faust")
    fs.create_file("/music/C/Current93/Faust/song1.flac")


def test_list_all_albums(fake_fs):
    expected = ["/music/A/Alio Die/Apsaras", "/music/B/Backworld/Isles"]
    result = Lossy.list_all_albums("/music")

    assert result == expected, f"Expected {expected}, but got {result}"
