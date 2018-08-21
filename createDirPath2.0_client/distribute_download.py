import os
import requests


class Download(object):
    def __init__(self, save_path, load_path):
        self.save_path = save_path
        self.load_path = load_path

    def download(self):
        load_path = self.load_path.split('/')[-1]
        save_path = self.save_path + os.sep + load_path
        r = requests.get(self.load_path, stream=True)
        f = open(save_path, "wb")
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
        f.close()
