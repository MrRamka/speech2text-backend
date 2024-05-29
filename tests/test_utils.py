import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
import os
from werkzeug.datastructures import FileStorage
from io import BytesIO
from utils import is_file_valid, remove_file, process_file

ALLOWED_FILE_EXTENSIONS = ('mp3', 'wav', 'ogg')


# Тесты для is_file_valid
def test_is_file_valid_no_file():
    result, error = is_file_valid(None)
    assert result == False
    assert error == 'No file provided'


@pytest.mark.parametrize("filename", ["test.mp3", "test.wav", "test.ogg"])
def test_is_file_valid_valid_extensions(filename):
    file = FileStorage(filename=filename)
    result, error = is_file_valid(file)
    assert result == True
    assert error == None


@pytest.mark.parametrize("filename", ["test.txt", "test.mp4", "test.doc"])
def test_is_file_valid_invalid_extensions(filename):
    file = FileStorage(filename=filename)
    result, error = is_file_valid(file)
    assert result == False
    assert error == f'Invalid file format. Allowed formats: {", ".join(ALLOWED_FILE_EXTENSIONS)}'


# Тесты для remove_file
def test_remove_file(tmp_path):
    dummy_file_path = os.path.join(tmp_path, "dummy.txt")
    with open(dummy_file_path, 'w') as dummy_file:
        dummy_file.write("dummy content")
    assert os.path.exists(dummy_file_path)
    remove_file(dummy_file_path)
    assert not os.path.exists(dummy_file_path)


# Тесты для process_file
def test_process_file(tmp_path):
    file = FileStorage(stream=BytesIO(b"dummy content"), filename="dummy.mp3")
    file_path = process_file(file, tmp_path)
    assert os.path.exists(file_path)
    assert os.path.basename(file_path) == "dummy.mp3"
    with open(file_path, 'rb') as saved_file:
        assert saved_file.read() == b"dummy content"
