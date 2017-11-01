import threading

class EnableAble(object):
    enable_lock = threading.Lock()

    def __init__(self):
        self._enable = True
    
    def _switch_enable(self, enable_state):
        self.enable_lock.acquire()
        self._enable = enable_state
        self.enable_lock.release()

    def disable(self):
        self._switch_enable(False)

    def enable(self):
        self._switch_enable(True)