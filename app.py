import re
from http import HTTPStatus

from flask import Flask, request

app = Flask(__name__)


@app.get("/")
def index() -> str:
    return ""


@app.route('/restore', methods=['POST'])
def restore():
    data = request.get_json()
    file_id = data['file_id']
    if not re.match("^[A-Za-z0-9]+$", file_id):
        return 'Invalid file_id!', HTTPStatus.BAD_REQUEST

    file_path = 'resources/' + file_id

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except FileNotFoundError as e:
        app.logger.error(e)
        return f'Unable to locate file_id {file_id}!', HTTPStatus.NOT_FOUND

    return content, HTTPStatus.OK


if __name__ == "__main__":
    app.run(debug=True)
