from google.cloud import storage
import io
import traceback
import base64


def get_uri_from_file(filename, filedata):
    try:
        client = storage.Client()
        bucket = client.lookup_bucket("aforaccessibility")
        if bucket == None:
            bucket = client.create_bucket("aforaccessibility")
    
        if bucket.get_blob(filename) != None:
            return False, "Tried to create file that already exists"
    
        blob = bucket.blob(filename)
        blob.upload_from_file(filedata)
        return blob.self_link
    except Exception as e:
        traceback.print_exc()