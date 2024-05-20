import os

ALLOWED_FILE_EXTENSIONS = ('mp3', 'wav', 'ogg')


def is_file_valid(file):
    if not file:
        return False, 'No file provided'

    file_name = file.filename

    if not file_name.lower().endswith(ALLOWED_FILE_EXTENSIONS):
        return False, 'Invalid file format. Allowed formats: mp3, wav, ogg'

    return True, None


def remove_file(file_path):
    os.remove(file_path)


def process_file(file, path):
    file_path = os.path.join(path, file.filename)
    file.save(file_path)

    return file_path
