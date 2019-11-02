from google.cloud import storage


def get_uri_from_file(filename, source_path):
    client = storage.Client()
    bucket = client.lookup_bucket("AForAccessibility")
    if bucket == None:
        bucket = client.create_bucket("AForAccessibility")
    
    if bucket.get_blob(filename) != None:
        return False, "Tried to create file that already exists"
    
    blob = bucket.create_blob(filename)
    blob.upload_from_filename(source_path)
    return blob.self_link