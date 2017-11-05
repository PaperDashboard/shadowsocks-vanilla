from shadowsocks.api.sakura import SakuraAPI
from shadowsocks.objects.user import User
from shadowsocks.transfer import base
from shadowsocks import config

class WebTransfer(base.BaseTransfer):
    def __init__(self):
        self._api = SakuraAPI(config.SITE_URL, config.SITE_KEY)

    def pull_user(self):
        users = self._api.getAllUser()
        for user in users:
            user["password"] = user["linkPassword"]
            del user["linkPassword"]
        return [User(u) for u in users]
    
    def run(self):
        super(WebTransfer, self).run()