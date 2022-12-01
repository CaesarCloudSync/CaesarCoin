import requests
import os
filename = "HusseyCoin.txt"
os.system(f"webtorrent create {filename} -o {filename}.torrent")
r = requests.post("http://127.0.0.1:5000/upload_torrent_file",files={"file":open(f"{filename}.torrent")})
print(r.content)

with open("man.txt.torrent","wb") as f:
    f.write(r.content)