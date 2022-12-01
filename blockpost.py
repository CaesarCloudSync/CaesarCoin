import requests
from requests_toolbelt.multipart import encoder

session = requests.Session()
with open('my_file.csv', 'rb') as f:
    form = encoder.MultipartEncoder({
        "documents": ("my_file.csv", f, "application/octet-stream"),
        "composite": "NONE",
    })
    headers = {"Prefer": "respond-async", "Content-Type": form.content_type}
    resp = session.post(url, headers=headers, data=form)
session.close()