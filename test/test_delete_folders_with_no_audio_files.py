from os.path import exists

import pytest

from src.delete_empty_folders import is_folder_empty
from src.delete_folder_with_no_audio_files import get_all_extensions, list_folders_with_no_audio_files, \
    delete_files_in_folder, delete_folders_with_no_audio_files
from src.exceptions import AudioFileDeleteErr


def test_get_all_extensions(fs):
    fs.create_dir("/Music/C/Current93/Faust")
    fs.create_file("/Music/C/Current93/Faust/song1.flac")
    fs.create_file("/Music/C/song2.mp3")
    fs.create_file("/Music/song3.wav")

    assert get_all_extensions("Music") == {"mp3", "flac", "wav"}


@pytest.fixture()
def fake_complicated_fs(fs):
    # normal depth = no audio here: should be deleted
    fs.create_dir("/Music/A/Anoemonia/Moonlit")
    fs.create_file("/Music/A/Anoemonia/Moonlit/ane - .cue")
    fs.create_file("/Music/A/Anoemonia/Moonlit/ane - .log")
    fs.create_file("/Music/A/Anoemonia/Moonlit/ane1 - .jpg")
    fs.create_file("/Music/A/Anoemonia/Moonlit/ane2 - .jpg")

    # one level deeper depth = no audio here: should be deleted
    fs.create_dir("/Music/A/Ataraxia/Lost Atlantis/Cover")
    fs.create_file("/Music/A/Ataraxia/Lost Atlantis/Cover/CD1.jpg")
    fs.create_file("/Music/A/Ataraxia/Lost Atlantis/Cover/CD2.jpg")
    fs.create_file("/Music/A/Ataraxia/Lost Atlantis/Cover/CD1.png")
    fs.create_file("/Music/A/Ataraxia/Lost Atlantis/Cover/CD2.png")

    # one level deeper depth = some audio here: should not be deleted
    fs.create_dir("/Music/A/Ataraxia/Spasm/")
    fs.create_file("/Music/A/Ataraxia/Spasm/CD1/1.flac")
    fs.create_file("/Music/A/Ataraxia/Spasm/CD1/2.flac")


def test_list_folders_with_no_audio_files(fake_complicated_fs):
    res = list_folders_with_no_audio_files("/Music")
    assert set(res) == {"/Music/A/Ataraxia/Lost Atlantis/Cover", "/Music/A/Anoemonia/Moonlit"}

def test_delete_folders_with_no_audio_files(fake_complicated_fs):
    assert exists("/Music/A/Anoemonia/Moonlit")
    assert exists("/Music/A/Ataraxia/Lost Atlantis/Cover")
    delete_folders_with_no_audio_files("/Music")
    assert not exists("/Music/A/Anoemonia/Moonlit")
    assert not exists("/Music/A/Ataraxia/Lost Atlantis/Cover")


@pytest.mark.parametrize("folder_path", [
    "/Music/A/Ataraxia/Lost Atlantis/Cover",
    "/Music/A/Anoemonia/Moonlit"
])
def test_delete_files_in_folder_success(fake_complicated_fs, folder_path):
    assert not is_folder_empty(folder_path)
    delete_files_in_folder(folder_path)
    assert is_folder_empty(folder_path)


def test_delete_files_in_folder_exception(fake_complicated_fs):
    folder_path = "/Music/A/Ataraxia/Spasm/CD1"
    assert not is_folder_empty(folder_path)
    with pytest.raises(AudioFileDeleteErr):
        delete_files_in_folder(folder_path)

    assert not is_folder_empty(folder_path)



