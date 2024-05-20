import asyncio
from flask import Flask, request, jsonify
from utils import process_file, remove_file, is_file_valid
from model import model_predict

UPLOAD_FOLDER = './user_files/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MODEL_PREDICT_TIMEOUT'] = 2


@app.route('/upload', methods=['POST'])
async def upload():
    file = request.files.get('file')

    is_valid, message = is_file_valid(file)

    if not is_valid:
        return jsonify({'error': message}), 400

    file_path = process_file(file, app.config['UPLOAD_FOLDER'])

    try:
        result, is_ok = await asyncio.wait_for(model_predict(file_path), timeout=int(app.config['MODEL_PREDICT_TIMEOUT']))

        if not is_ok:
            return jsonify({'message': result}), 500

        return jsonify({'message': result}), 200
    except asyncio.TimeoutError:
        return jsonify({'error': 'Request timed out'}), 500
    except Exception:
        return jsonify({'error': 'Request error'}), 500
    finally:
        remove_file(file_path)


if __name__ == '__main__':
    app.run()
