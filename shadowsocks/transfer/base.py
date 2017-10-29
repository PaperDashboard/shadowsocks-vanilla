from shadowsocks.event.server_pool import ServerPool
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
        return [{
            "passwd": "testLink",
            "method": "rc4-md5",
            "port": 1234
        }]

    @staticmethod
    def run():
        while True:
            users = BaseTransfer.get_instance().pull_user();
            for user in users:
                if not ServerPool.get_instance().server_is_run(int(user["port"])):
                    ServerPool.get_instance().new_server(int(user["port"]), user["passwd"], user["method"])

            time.sleep(60)