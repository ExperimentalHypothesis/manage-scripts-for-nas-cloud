import pytest

from src.lossy import list_albums


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
