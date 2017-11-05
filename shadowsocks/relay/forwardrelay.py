from shadowsocks.trains import traffic_able, enable_able
import threading
import logging
import socket

class ForwardRelayHelper(threading.Thread, enable_able.EnableAble):
    def __init__(self, source, to):
        threading.Thread.__init__(self)
        enable_able.EnableAble.__init__(self)
        self.source = source
        self.to = to

    def run(self):
        while self.get_enable():
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
        logging.info("starting forward port in %s" % port)

    def init(self):
        self._l_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._l_sock.bind(('', self.port))
        self._l_sock.listen(1024)
        self.setDaemon(True)

    def run(self):
        helper_a, helper_b = None, None
        try:
            while self.get_enable():
                client_socket, address = self._l_sock.accept()
                logging.info("resive connect from %s" % address[0])
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.connect((self.to, self.to_port))
                helper_a = ForwardRelayHelper(client_socket, server_socket)
                helper_b = ForwardRelayHelper(server_socket, client_socket)
                helper_a.setDaemon(True)
                helper_b.setDaemon(True)
                helper_a.start()
                helper_b.start()
        except Exception:
            helper_a.disable()
            helper_b.disable()
            self.disable()
