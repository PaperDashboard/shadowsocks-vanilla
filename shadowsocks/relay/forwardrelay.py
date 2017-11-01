from shadowsocks.trains import traffic_able, enable_able
import threading

class ForwardRelay(threading.Thread, traffic_able.TrafficAbl, enable_able.EnableAble):
    def __init__(self):
        threading.Thread.__init__(self)
        enable_able.EnableAble.__init__(self)

    def run(self):
        pass