from shadowsocks.transfer.base import BaseTransfer
from shadowsocks.transfer.file import FileTransfer
import logging
import thread
import time

if __name__ == "__main__":
    thread.start_new_thread(FileTransfer.run, (FileTransfer("shadowsocks.json"),))

    logging.basicConfig(format="[%(asctime)s][%(levelname)-5s] > %(filename)-15s[%(lineno)-4s] %(message)s")
    logging.getLogger().setLevel(logging.DEBUG)   
 
    while True:
        time.sleep(60)