import logging
import os.path

import pytest

from src.delete_empty_folders import is_folder_empty, list_all_empty_folders, delete_folder, delete_empty_folders


@pytest.fixture
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


@pytest.mark.parametrize("folder_path, expected",
                         [
                             ("/Music/A/Alio Die", True),
                             ("/Music/Z", True),
                             ("/Music/B/Backworld/Isles", False),
                             ("Music/C/Current93/Faust", False),
                         ])
def test_is_empty(fake_fs, folder_path, expected):
    assert is_folder_empty(folder_path) is expected


def test_list_all_empty_folders(fake_fs):
    res = list_all_empty_folders("/Music")
    assert res == ["/Music/A/Alio Die", "/Music/Z"]


@pytest.mark.parametrize("folder_path",
                         [
                             "/Music/Z",
                             "/Music/A/Alio Die",
                         ]
                         )
def test_delete_folder_success(fake_fs, folder_path, caplog):
    assert os.path.exists(folder_path)

    with caplog.at_level(logging.WARNING):
        delete_folder(folder_path)

    assert f"Deleted folder on path {folder_path}"
    assert not os.path.exists(folder_path)


@pytest.mark.parametrize("folder_path",
                         [
                             "/Music/B/Backworld/Isles",
                             "/Music/C/Current93/Faust",
                         ]
                         )
def test_delete_folder_exception(fake_fs, folder_path, caplog):
    assert os.path.exists(folder_path)
    with caplog.at_level(logging.ERROR):
        delete_folder(folder_path)

    assert f"Could not delete folder on path {folder_path}"
    assert os.path.exists(folder_path)


def test_delete_empty_folders(fake_fs):
    assert os.path.exists("/Music/A/Alio Die")
    assert os.path.exists("/Music/Z")

    delete_empty_folders("/Music")

    assert not os.path.exists("/Music/A/Alio Die")
    assert not os.path.exists("/Music/A")
    assert not os.path.exists("/Music/Z")

    assert os.path.exists("/Music/B/Backworld/Isles")
    assert os.path.exists("/Music/C/Current93/Faust")



