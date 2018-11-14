import os
import requests
import threadpool


class Download(object):
    def __init__(self, save_path, load_path):
        self.save_path = save_path
        self.load_path = eval(load_path)
        self.pool = threadpool.ThreadPool(3)

    def putThread(self):
        if len(self.load_path) != 1:
            requests = threadpool.makeRequests(self.download, self.load_path)
            [self.pool.putRequest(req) for req in requests]
        else:
            self.download(self.load_path[0])

    def download(self, load_path):
        fileName = load_path.split('/')[-1]
        save_path = self.save_path + os.sep + fileName
        r = requests.get(load_path, stream=True)
        f = open(save_path, "wb")
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
        f.close()
