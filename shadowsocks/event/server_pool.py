#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 clowwindy
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from shadowsocks.relay import tcprelay
from shadowsocks.relay import udprelay
from shadowsocks.async import asyncdns
from shadowsocks.utils import utils
from shadowsocks import config
from socket import *
import eventloop
import threading
import logging
import thread
import time
import sys
import os

class ServerPool(object):

    instance = None

    def __init__(self):
        # utils.check_python()
        # self.config = utils.get_config(False)
        self.config = config
        # utils.print_shadowsocks()
        self.dns_resolver = asyncdns.DNSResolver()
        self.tcp_servers_pool = {}
        self.udp_servers_pool = {}

        self.loop = eventloop.EventLoop()
        thread.start_new_thread(ServerPool._loop, (self.loop, self.dns_resolver))

    @staticmethod
    def get_instance():
        if ServerPool.instance is None:
            ServerPool.instance = ServerPool()
        return ServerPool.instance

    @staticmethod
    def _loop(loop, dns_resolver):
        try:
            dns_resolver.add_to_loop(loop)
            loop.run()
        except (KeyboardInterrupt, IOError, OSError) as e:
            logging.error(e)
            import traceback
            traceback.print_exc()
            os.exit(0)

    def server_is_run(self, user):
        if user.id in self.tcp_servers_pool:
            return True
        return False

    def new_server(self, user):
        ret = True
        port = int(user.port)

        if user.id in self.tcp_servers_pool:
            logging.info("server already at %s:%d" % (config.server, port))
            return 'this port server is already running'
        else:
            a_config = {
                "server": config.SERVER,
                "timeout": config.TIMEOUT,
                "fast_open": config.FAST_OPEN,
                "method": user.method,
                "crypto_path": {}
            }
            a_config['server_port'] = port
            a_config['password'] = user.password
            try:
                logging.info("starting server at %s:%d" % (a_config['server'], port))
                tcp_server = tcprelay.TCPRelay(a_config, self.dns_resolver, False)
                tcp_server.add_to_loop(self.loop)
                self.tcp_servers_pool[user.id] = tcp_server
                udp_server = udprelay.UDPRelay(a_config, self.dns_resolver, False)
                udp_server.add_to_loop(self.loop)
                self.udp_servers_pool[user.id] = udp_server
            except Exception, e:
                logging.warn(e)
        return True

    def del_server(self, user):
        port = int(user.port)

        if user.id not in self.tcp_servers_pool:
            logging.info("stopped server at %s:%d already stop" % (config.SERVER, port))
        else:
            logging.info("stopped server at %s:%d" % (config.SERVER, port))
            # try:
            try:
                self.tcp_servers_pool[user.id].close()
                del self.tcp_servers_pool[user.id]
                self.udp_servers_pool[user.id].close()
                del self.udp_servers_pool[user.id]
            except Exception, e:
                logging.warn(e)
            return True

    def get_port_transfer(self, user):
        ret = 0L
        #this is different thread but safe
        t_servers = self.tcp_servers_pool.copy()
        u_servers = self.udp_servers_pool.copy()

        if user.id in t_servers:
            ret += t_servers[user.id].get_download()
            ret += t_servers[user.id].get_upload()

        if user.id in u_servers:
            ret += u_servers[user.id].get_download()
            ret += u_servers[user.id].get_upload()

        return ret
