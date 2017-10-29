class User(object):
    def __init__(self, config):
        self.port = int(config["port"])
        self.password = str(config["password"])
        self.method = str(config["method"])

    
    def __eq__(self, other):
        return self.port == other.port and self.password == other.password and self.method == other.method