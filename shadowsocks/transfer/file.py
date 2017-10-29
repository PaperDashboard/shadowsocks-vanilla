from shadowsocks.objects.user import User
from shadowsocks.transfer import base
import json

class FileTransfer(base.BaseTransfer):
    def __init__(self, file):
        self._path = file

    def pull_user(self):
        with open(self._path, "r") as file:
           return [User(item) for item in json.loads(file.read())]

    def run(self):
        super(FileTransfer, self).run()
