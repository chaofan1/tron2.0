#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
# 将服务器执行成功的命令告诉数据库


import urllib
import urllib2


class CallBack:
    def __init__(self):
        self.url = ''
        self.query_args = {}

    def callback(self, command_id):
        self.url = 'http://192.168.100.49/tron/index.php/python/renewScriptStatus'
        self.query_args = {'id': command_id}
        self.request()

    def callback_pack(self, pack_id):
        self.url = 'http://192.168.100.49/tron/index.php/python/callback_pack_status'
        self.query_args = {'id': pack_id}
        self.request()

    def callback_transit(self, transit_id):
        self.url = 'http://192.168.100.49/tron/index.php/python/distribute/callback'
        self.query_args = {'command_id': transit_id}
        self.request()

    def request(self):
        encoded_args = urllib.urlencode(self.query_args)
        try:
            response = urllib2.urlopen(self.url, encoded_args)
        except urllib2.HTTPError, e:
            print e.code
        except urllib2.URLError, e:
            print e.reason
        else:
            print response.read()

