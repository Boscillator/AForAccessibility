from flask import Flask, request
from werkzeug.utils import secure_filename
import json
import os
import glob
import base64
from STT_utils import stt_from_uri
from GCS_utils import get_uri_from_file
from google.cloud import storage


app = Flask(__name__)
UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = set(["wav", "txt"])


def allowed_file(filename):
    return filename.count('.') == 1 \
        and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/upload', methods=['POST'])
def upload_file():
    post_data = request.form
    if "filename" not in post_data \
            or "filedata" not in post_data \
            or "timestamp" not in post_data:
        return json.dumps({"status": "failure", "message": "Incomplete data in POST message body"})
    if post_data["filename"] == '':
        return json.dumps({"status": "failure", "message": "No file name discovered"})
    if allowed_file(post_data["filename"]):
        filename = secure_filename(post_data["filename"])
        with open(os.path.join(UPLOAD_FOLDER, filename), "wb") as fp:
            fp.write(base64.b64decode(post_data["filedata"]))
        return json.dumps({"status": "success", "message": "Uploaded file"})

    return json.dumps({"status": "failure", "message": "File name/type not permitted"})


@app.route("/test")
def hello_world():
    with open("./test.html", "r") as fp:
        result = "".join(fp.readlines())
        return result


if __name__ == "__main__":
    app.run(debug=True)
