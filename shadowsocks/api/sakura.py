import urllib2
import json

def _get_with_key(url, key):
    req = urllib2.Request(url=url, headers={
        "x-key": key
    })
    res = urllib2.urlopen(req)
    return json.load(res)

def _post_with_key(url, key, data):
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(url, data=data)
    request.add_header('Content-Type', 'application/json')
    request.add_header('X-Key', key)
    request.get_method = lambda: 'PUT'
    res = opener.open(request)
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

    def addTraffic(self, user, traffic): 
        return _post_with_key(
            self._site + "/user/" + user.id + "/addTraffic",
            self._api_key,
            json.dumps({"value": traffic})
        )