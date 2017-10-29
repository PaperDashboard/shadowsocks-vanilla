from shadowsocks.event.server_pool import ServerPool
from shadowsocks.objects.user import User
import logging
import time


class BaseTransfer(object):
    instance = None

    @staticmethod
    def get_instance():
        if not BaseTransfer.instance:
            BaseTransfer.instance = BaseTransfer()

        return BaseTransfer.instance

    @staticmethod
    def pull_user():
        return [User({
            "password": "testLink",
            "method": "rc4-md5",
            "port": 1234
        })]

    def run(self):
        return run(self)

def run(transfer):
    olderUser = []
    while True:
        users = transfer.pull_user();

        for ouser in olderUser:
            if not ouser in users:
                ServerPool.get_instance().del_server(ouser)
        
        olderUser = users
        logging.info("polling")
        for user in users:
            if not ServerPool.get_instance().server_is_run(user):
                ServerPool.get_instance().new_server(user)

        time.sleep(10)