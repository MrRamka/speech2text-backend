import json
import os
import wave

import vosk

vosk_model_filename = "vosk-model-small-ru-0.22"


async def model_predict(file_path):
    if not os.path.exists(vosk_model_filename):
        return "No audio model", False

    model = vosk.Model(vosk_model_filename)

    wf = wave.open(file_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        return "Audio file must be WAV format mono PCM.", False

    rec = vosk.KaldiRecognizer(model, wf.getframerate())

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            print(rec.Result())

    result = rec.FinalResult()

    return json.loads(result), True
