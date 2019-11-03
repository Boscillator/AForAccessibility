import requests
from datetime import datetime
import base64
import json
import sys


data = {
    "filename": sys.argv[1],
    "timestamp": int(datetime.now().strftime("%s")),
}
fdata = ""
with open("/mnt/c/Users/Sam Cohen/Downloads/Useful Idiots - Sanders Interview - snipped.wav", "rb") as fp:
    fdata = fp.read()

print(type(base64.b64encode(fdata).decode("ASCII")))
data["filedata"] = base64.b64encode(fdata).decode("ASCII")
#data["filedata"] = base64.b64encode(fdata)

print(requests.post("http://localhost:5000/api/upload", data=data).text)