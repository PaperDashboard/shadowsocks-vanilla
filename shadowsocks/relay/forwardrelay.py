from shadowsocks.trains import traffic_able, enable_able
import threading
import socket

class ForwardRelayHelper(threading.Thread):
    def __init__(self, source, to):
        threading.Thread.__init__(self)
        self.source = source
        self.to = to

    def run(self):
        while True:
            s = self.source.recv(1024)
            if s:
                self.to.sendall(s)
            else:
                self.source.shutdown(socket.SHUT_RD)
                self.to.shutdown(socket.SHUT_WR)
                return None

class ForwardRelay(threading.Thread, traffic_able.TrafficAble, enable_able.EnableAble):
    def __init__(self, port, to, to_port):
        threading.Thread.__init__(self)
        enable_able.EnableAble.__init__(self)
        self.port = port
        self.to = to
        self.to_port = to_port
        self.init()

    def init(self):
        self._l_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._l_sock.bind(('', self.port))
        self._l_sock.listen(1024)

    def run(self):
        while self.get_enable():
            client_socket = self._l_sock.accept()[0]
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((self.to, self.to_port))
            ForwardRelayHelper(client_socket, server_socket).start()
            ForwardRelayHelper(server_socket, client_socket).start()

