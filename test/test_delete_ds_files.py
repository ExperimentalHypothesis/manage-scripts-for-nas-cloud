import os.path

from contextlib import nullcontext as no_exception
from os.path import exists

import pytest

from src.delete_ds_files import list_all_ds_filepaths, has_only_ds_file, delete_file, delete_all_ds_files


@pytest.fixture  # TODO use conftest
def fake_fs(fs):
    # Empty
    fs.create_dir("/Music/A/Alio Die")

    # Empty
    fs.create_dir("/Music/Z")

    # Only .DS file
    fs.create_dir("/Music/B/Backworld/Isles")
    fs.create_file("/Music/B/Backworld/Isles/.DS_Store")

    # Not empty
    fs.create_dir("/Music/C/Current93/Faust")
    fs.create_file("/Music/C/Current93/Faust/song1.flac")
    fs.create_file("/Music/C/Current93/Faust/.DS_Store")
    fs.create_file("/Music/C/Current93/.DS_Store")


@pytest.mark.parametrize("folder_path, expected",
                         [
                             ("/Music/A/Alio Die", False),
                             ("/Music/Z", False),
                             ("/Music/B/Backworld/Isles", True),
                             ("/Music/C/Current93/Faust", False),
                         ])
def test_has_only_ds_file(fake_fs, folder_path, expected):
    assert has_only_ds_file(folder_path) is expected


def test_list_all_ds_filepaths(fake_fs):
    res = list_all_ds_filepaths("/Music")
    assert set(res) == {"/Music/B/Backworld/Isles/.DS_Store",
                        "/Music/C/Current93/Faust/.DS_Store",
                        "/Music/C/Current93/.DS_Store"}


def test_delete_file_success(fake_fs):
    assert exists("/Music/B/Backworld/Isles/.DS_Store")
    delete_file("/Music/B/Backworld/Isles/.DS_Store")
    assert not exists("/Music/B/Backworld/Isles/.DS_Store")


def test_delete_file_exception(fake_fs):
    assert exists("/Music/C/Current93/Faust/song1.flac")
    with pytest.raises(RuntimeError) as err:
        delete_file("/Music/C/Current93/Faust/song1.flac")

    assert "Filepath /Music/C/Current93/Faust/song1.flac does not contain DS_Store file" == str(err.value)
    assert exists("/Music/C/Current93/Faust/song1.flac")


def test_delete_all_ds_files(fake_fs):
    assert exists("/Music/B/Backworld/Isles/.DS_Store")
    assert exists("/Music/C/Current93/Faust/.DS_Store")
    assert exists("/Music/C/Current93/.DS_Store")

    delete_all_ds_files("/Music")

    assert not exists("/Music/B/Backworld/Isles/.DS_Store")
    assert not exists("/Music/C/Current93/Faust/.DS_Store")
    assert not exists("/Music/C/Current93/.DS_Store")
