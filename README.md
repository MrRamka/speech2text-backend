# Speech to Text backend

## Environment
### Python
```bash
python3 --version
Python 3.10.4
```

### pip
```bash
pip --version
pip 23.2.1
```

### Install dependencies
```bash
pip install -r requirements.txt
```

## Model 
1. Нужно скачать модель с сайта https://alphacephei.com/vosk/models
2. Распаковать в корень проекта

Для теста использовалась `vosk-model-small-ru-0.22`

## Start application

### Debug

```bash
flask --app upload run --debug
```
