class User(object):
    def __init__(self, config):
        self.port = int(config["port"])
        self.password = str(config["password"])
        self.method = str(config["method"])
        if "_id" in config:
            self.id = config["_id"]["$oid"]
        else:
            self.id = str(self.port)

    def __eq__(self, other):
        return (self.port == other.port and 
            self.password == other.password and 
            self.method == other.method and 
            self.id == other.id)