import pytest

from src.split_flac_on_cue import has_one_cue_for_one_flac


@pytest.fixture
def fake_fs(fs):
    fs.create_dir("/Music/B/Backworld/Isles")
    fs.create_file("/Music/B/Backworld/Isles/song.flac")
    fs.create_file("/Music/B/Backworld/Isles/song.cue")

    fs.create_dir("/Music/B/Baby Dee/Album")
    fs.create_file("/Music/B/Baby Dee/Album/song1.flac")
    fs.create_file("/Music/B/Baby Dee/Album/song2.flac")
    fs.create_file("/Music/B/Baby Dee/Album/song.cue")

    fs.create_dir("/Music/C/Current93/Faust")
    fs.create_file("/Music/C/Current93/Faust/song.cue")



def test_has_one_cue_for_one_flac(fake_fs):
    res = has_one_cue_for_one_flac("/Music/B/Backworld/Isles")
    assert res is True

    res = has_one_cue_for_one_flac("/Music/B/Baby Dee/Album")
    assert res is False

    res = has_one_cue_for_one_flac("/Music/C/Current93/Faust")
    assert res is False


