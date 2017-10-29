from shadowsocks.transfer.base import BaseTransfer
from shadowsocks.transfer.file import FileTransfer
import logging
import thread
import time

if __name__ == "__main__":
    thread.start_new_thread(FileTransfer.run, (FileTransfer("shadowsocks.json"),))

    logging.basicConfig(format="%(filename)s %(lineno)d %(process)d %(message)s")
    logging.getLogger().setLevel(logging.DEBUG)   
 
    while True:
        time.sleep(60)