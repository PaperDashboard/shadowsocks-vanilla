import urllib2
import json

def _get_with_key(url, key):
    req = urllib2.Request(url=url, headers={
        "x-key": key
    })
    res = urllib2.urlopen(req)
    return json.load(res)

class SakuraAPI(object):
    def __init__(self, site, api_key):
        self._site = site
        self._api_key = api_key

    def getAllUser(self):
        return _get_with_key(
            self._site + "/users",
            self._api_key
        )