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
import wave
import traceback
import io
import pymongo
from reports import process_report


def get_mongo_db():
    if "AFA_MONGO_USERNAME" not in os.environ:
        print("ERROR: MongoDB username unset")
        return
    if "AFA_MONGO_PASSWORD" not in os.environ:
        print("ERROR: MongoDB username unset")
        return
    db_username = os.environ["AFA_MONGO_USERNAME"]
    db_password = os.environ["AFA_MONGO_PASSWORD"]
    client = pymongo.MongoClient(f"mongodb+srv://{db_username}:{db_password}@a-for-accessibility-p2keg.gcp.mongodb.net/test?retryWrites=true&w=majority")
    db = client["test"]
    return db


def upload_file(uid, filename, filedata, timestamp):
    try:
        filename = secure_filename(filename)
        decoded = base64.b64decode(filedata)
        filedata = io.BytesIO(decoded)
        gcs_uri = get_uri_from_file(uid + ".wav", filedata)
        sample_rate = 16000
        filedata.seek(0)
        with wave.open(filedata) as fp:
            sample_rate = fp.getframerate()
        stt_uri = "gs://aforaccessibility/" + uid + ".wav"
        stt_data = stt_from_uri(stt_uri, sample_rate)

        report = process_report(stt_data)

        db = get_mongo_db()
        post = {
            "_id": uid,
            "gcs_audio": stt_uri,
            "public_audio": gcs_uri,
            "file_name": filename,
            "report": report
        }
        db["reports"].insert_one(post)
        print("Successfully processed and saved report")
    except Exception as e:
        traceback.print_exc()


app = Flask(__name__)
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
        process_pool.apply_async(
            upload_file, (uid, filename, post_data["filedata"], post_data["timestamp"]))
        return json.dumps({"status": "success", "message": "Uploaded file", "uid": uid})

    return json.dumps({"status": "failure", "message": "File name/type not permitted"}), 400


@app.route('/api/report/<string:uid>', methods=["GET"])
def get_report(uid):
    db = get_mongo_db()
    result = db["reports"].find_one({"_id": uid})
    if result == None:
        return json.dumps({"status": "failure", "message": "Could not find a document with that _id"}), 404
    return json.dumps(result["report"])


@app.route('/api/reports', methods=["GET"])
def get_all_reports():
    db = get_mongo_db()
    results = [
        {
            "uid": doc["_id"],
            "filename": doc["file_name"]
        }
        for doc in db["reports"].find()]

    return json.dumps(results)


@app.route("/test")
def hello_world():
    with open("./test.html", "r") as fp:
        result = "".join(fp.readlines())
        return result


if __name__ == "__main__":
    app.run(debug=True)
