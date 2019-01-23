#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# 将服务器执行成功的命令告诉数据库

import time
import urllib
import urllib2
import socket
import logging
from config import log_path_server


class CallBack:
    def __init__(self):
        logging.basicConfig(filename=log_path_server + time.strftime("%Y%m%d") + '.log', level=logging.INFO,
                            format="%(asctime)s - %(levelname)s - %(message)s")
        self.url = ''
        self.query_args = {}
        self.ip = socket.gethostbyname(socket.gethostname())

    def callback(self, command_id):
        self.url = 'http://%s/python/renewScriptStatus' % self.ip
        self.query_args = {'id': command_id}
        self.request_post()

    def callback_pack(self, pack_id):
        self.url = 'http://%s/python/callback_pack_status' % self.ip
        self.query_args = {'id': pack_id}
        self.request_get()

    def callback_transit(self, command_id):
        self.url = 'http://%s/python/distribute/callback' % self.ip
        self.query_args = {'command_id': command_id}
        self.request_get()

    def callback_transit_complete(self, transit_ids, user_id):
        self.url = 'http://%s/python/send_complete' % self.ip
        self.query_args = {'ids': transit_ids, 'user_id': user_id}
        self.request_get()

    def callback_download(self, id, user_id):
        self.url = 'http://%s/python/download_complete' % self.ip
        self.query_args = {'id': id, 'user_id': user_id}
        self.request_get()

    def request_post(self):
        encoded_args = urllib.urlencode(self.query_args)
        logging.info('URL:' + self.url, self.query_args)
        try:
            response = urllib2.urlopen(self.url, encoded_args)
        except urllib2.HTTPError, e:
            print e.code
            logging.info(e.code)
        except urllib2.URLError, e:
            print e.reason
            logging.info(e.reason)
        else:
            print response.read()
            logging.info(response.read())

    def request_get(self):
        word = urllib.urlencode(self.query_args)
        newurl = self.url + "?" + word
        logging.info('URL:' + newurl)
        request = urllib2.Request(newurl)
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            print e.code
            logging.info(e.code)
        except urllib2.URLError, e:
            print e.reason
            logging.info(e.reason)
        else:
            print response.read()
            logging.info(response.read())


if __name__ == '__main__':
    CallBack().callback(1)