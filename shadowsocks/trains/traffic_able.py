import threading

class TrafficAble(object):
    upload_traffic = 0L
    upload_lock = threading.Lock()

    download_traffic = 0L
    download_lock = threading.Lock()

    def __init__(self):
        # Dont't need
        pass

    def add_upload(self, number):
        self.upload_lock.acquire()
        self.upload_traffic += number
        self.upload_lock.release()

    def add_download(self, number):
        self.download_lock.acquire()
        self.download_traffic += number
        self.download_lock.release()

    def get_download(self):
        self.download_lock.acquire()
        num = self.download_traffic
        self.download_lock.release()
        return num

    def get_upload(self):
        self.upload_lock.acquire()
        num = self.upload_traffic
        self.upload_lock.release()
        return num