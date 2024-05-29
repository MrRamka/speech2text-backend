import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
import os
from unittest.mock import patch, MagicMock, AsyncMock

from model import model_predict

# Для удобства создадим поддельный путь к файлу
file_path = "fake_audio.wav"


@pytest.mark.asyncio
@patch("os.path.exists", return_value=False)
async def test_no_model_dir(mock_wave_open):
    result, success = await model_predict(file_path)

    assert result == "No audio model"
    assert not success


@pytest.mark.asyncio
@patch("wave.open")
@patch("vosk.Model", autospec=True)
@patch("os.path.exists", return_value=True)  # Утверждаем что модель существует
async def test_invalid_audio_file(mock_exists, mock_model, mock_wave_open):
    # Мокируем объект wave
    wf = MagicMock()
    wf.getnchannels.return_value = 2  # Мокируем неправильное значение
    wf.getsampwidth.return_value = 2
    wf.getcomptype.return_value = "NONE"
    mock_wave_open.return_value = wf

    result, success = await model_predict(file_path)

    assert result == "Audio file must be WAV format mono PCM."
    assert not success


@pytest.mark.asyncio
@patch("wave.open")
@patch("vosk.KaldiRecognizer", autospec=True)
@patch("vosk.Model", autospec=True)  # Мокируем создание модели vosk
@patch("os.path.exists", return_value=True)  # Утверждаем что модель существует
async def test_valid_audio_file(mock_exists, mock_model, mock_kaldi_recognizer, mock_wave_open):
    # Мокируем объект wave
    wf = MagicMock()
    wf.getnchannels.return_value = 1
    wf.getsampwidth.return_value = 2
    wf.getcomptype.return_value = "NONE"
    wf.readframes.side_effect = [b"data", b""]  # Возвращаем данные и затем пустой байт
    wf.getframerate.return_value = 16000  # Пример частоты дискретизации
    mock_wave_open.return_value = wf

    # Мокируем объект калди рекогнайзер
    rec = MagicMock()
    rec.AcceptWaveform.return_value = True
    rec.Result = MagicMock(return_value=json.dumps({"text": "example"}))
    rec.FinalResult = MagicMock(return_value=json.dumps({"text": "final result"}))
    mock_kaldi_recognizer.return_value = rec

    result, success = await model_predict(file_path)

    assert isinstance(result, dict)
    assert result.get("text") == "final result"
    assert success