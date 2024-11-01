import subprocess
from unittest.mock import call

import pytest

from src.split_flac_on_cue import has_one_cue_for_one_flac, get_cue_pathfile, list_cue_files, split_flac_on_cue


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


def test_get_cue_pathfile(fake_fs):
    res = get_cue_pathfile("/Music/B/Backworld/Isles")
    assert res == "/Music/B/Backworld/Isles/song.cue"


def test_list_cue_files(fake_fs):
    res = list_cue_files("/Music")
    assert res == ["/Music/B/Backworld/Isles/song.cue"]


def test_split_flac_on_cue_any_order(mocker):
    cue_files = ['test2.cue', 'test1.cue']
    mock_run = mocker.patch('subprocess.run')

    split_flac_on_cue(cue_files)
    expected_calls = [
        call(['ffcuesplitter', '-i', 'test1.cue'], check=True),
        call(['ffcuesplitter', '-i', 'test2.cue'], check=True)
    ]
    mock_run.assert_has_calls(expected_calls, any_order=True)