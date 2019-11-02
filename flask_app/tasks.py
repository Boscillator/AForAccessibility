import base64
import os
from werkzeug.utils import secure_filename
from GCS_utils import get_uri_from_file
from app import celery, UPLOAD_FOLDER


@celery.task()
def upload_file(uid, filename, filedata, timestamp):
    filename = secure_filename(filename)
    filename = os.path.join(UPLOAD_FOLDER, filename)
    with open(filename, "wb") as fp:
        fp.write(base64.b64decode(filedata))
    gcs_uri = get_uri_from_file(uid + ".wav", filename)
    print(gcs_uri)