from shadowsocks.trains import traffic_able
import threading

class ForwardRelay(threading.Thread, traffic_able.TrafficAble):
    def __init__(self):
        threading.Thread.__init__(self)