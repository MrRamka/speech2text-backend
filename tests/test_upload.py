from io import BytesIO
from unittest.mock import patch, AsyncMock

import pytest

from upload import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@patch('upload.process_file', return_value='mocked_file_path')
@patch('upload.remove_file')
@patch('upload.model_predict', new_callable=AsyncMock)
@patch('upload.is_file_valid', return_value=(True, ''))
def test_upload_success(is_file_valid_mock, model_predict_mock, remove_file_mock, process_file_mock, client):
    model_predict_mock.return_value = ("{'text': 'message'}", True)

    data = {
        'file': (BytesIO(b'mocked data'), 'test.wav')
    }

    response = client.post('/upload', content_type='multipart/form-data', data=data)

    assert response.status_code == 200
    assert response.json == {'message': "{'text': 'message'}"}


@patch('upload.process_file', return_value='mocked_file_path')
@patch('upload.remove_file')
@patch('upload.model_predict', new_callable=AsyncMock)
@patch('upload.is_file_valid', return_value=(True, ''))
def test_upload_model_failure(is_file_valid_mock, model_predict_mock, remove_file_mock, process_file_mock, client):
    model_predict_mock.return_value = ("No audio model", False)

    data = {
        'file': (BytesIO(b'mocked data'), 'test.wav')
    }

    response = client.post('/upload', content_type='multipart/form-data', data=data)

    assert response.status_code == 500
    assert response.json == {'message': "No audio model"}


@patch('upload.process_file', return_value='mocked_file_path')
@patch('upload.remove_file')
@patch('upload.is_file_valid', return_value=(False, 'Invalid file'))
def test_upload_invalid_file(is_file_valid_mock, remove_file_mock, process_file_mock, client):
    data = {
        'file': (BytesIO(b'mocked data'), 'test.wav')
    }

    response = client.post('/upload', content_type='multipart/form-data', data=data)

    assert response.status_code == 400
    assert response.json == {'error': 'Invalid file'}