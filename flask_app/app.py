from flask import Flask, request
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import json
import os
import glob
import base64
from STT_utils import stt_from_uri
from GCS_utils import get_uri_from_file
from google.cloud import storage
import string
from celery import Celery
import random
from multiprocessing import Pool



def upload_file(uid, filename, filedata, timestamp):
    filename = secure_filename(filename)
    filename = os.path.join(UPLOAD_FOLDER, filename)
    with open(filename, "wb") as fp:
        fp.write(base64.b64decode(filedata))
    gcs_uri = get_uri_from_file(uid + ".wav", filename)
    print(gcs_uri)


app = Flask(__name__)
UPLOAD_FOLDER = "./uploads"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

process_pool = Pool(4)


def allowed_file(filename):
    return True


uid_str_options = string.ascii_lowercase + \
    string.ascii_lowercase + string.digits


def make_uid():
    return "".join([random.choice(uid_str_options) for _ in range(25)])


@app.route('/api/upload', methods=['POST'])
def api_receive_upload():
    post_data = request.json
    if "filename" not in post_data \
            or "filedata" not in post_data \
            or "timestamp" not in post_data:
        return json.dumps({"status": "failure", "message": "Incomplete data in POST message body"}), 400
    if post_data["filename"] == '':
        return json.dumps({"status": "failure", "message": "No file name discovered"}), 400
    if allowed_file(post_data["filename"]):
        filename = post_data["filename"] + ".wav"
        uid = make_uid()
        process_pool.apply_async(upload_file, (uid, filename, post_data["filedata"], post_data["timestamp"]))
        return json.dumps({"status": "success", "message": "Uploaded file", "uid": uid})

    return json.dumps({"status": "failure", "message": "File name/type not permitted"}), 400


@app.route('/api/report/id')
def get_report():
    # Give 404 on incomplete job
    print("hello world")
    return "", 404


@app.route("/test")
def hello_world():
    with open("./test.html", "r") as fp:
        result = "".join(fp.readlines())
        return result


if __name__ == "__main__":
    app.run(debug=True)
