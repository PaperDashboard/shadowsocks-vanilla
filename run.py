from shadowsocks.transfer.base import BaseTransfer
import logging
import thread
import time

if __name__ == "__main__":
    thread.start_new_thread(BaseTransfer.run, ())

    logging.basicConfig(format="%(filename)s %(lineno)d %(process)d %(message)s")
    logging.getLogger().setLevel(logging.DEBUG)   
 
    while True:
        time.sleep(60)