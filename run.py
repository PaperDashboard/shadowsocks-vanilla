from shadowsocks.transfer.base import BaseTransfer
from shadowsocks.transfer.file import FileTransfer
from shadowsocks.relay.forwardrelay import ForwardRelay
import logging
import thread
import time

if __name__ == "__main__":
    # thread.start_new_thread(FileTransfer.run, (FileTransfer("shadowsocks.json"),))

    logging.basicConfig(format="[%(asctime)s][%(levelname)s][AT: %(filename)s[%(lineno)s]] %(message)s")
    logging.getLogger().setLevel(logging.DEBUG)   
    
    relay = ForwardRelay(8080, "www.baidu.com", 80)
    relay.start()

    
    while True:
        try:
            time.sleep(60)
        except Exception:
            import sys
            relay.disable()
            sys.exit(0)