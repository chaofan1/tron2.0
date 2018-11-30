﻿#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Filename: httpUrl.py
# 将数据返回给服务器

import urllib
import urllib2


class CallBack:
    def __init__(self):
        self.url = ''
        self.query_args = {}

    def dai_callback(self, ID, path, file_name, img_size):
        self.url = 'http://192.168.100.49/callback/dailies'
        if img_size:
            self.query_args = {'id': ID, 'path': path, 'filename': file_name, 'imgSize': img_size}
        else:
            self.query_args = {'id': ID, 'path': path, 'filename': file_name}
        self.request()

    def render_callback(self, command_id):
        self.url = 'http://192.168.100.49/tron/index.php/python/renewScriptStatus'
        self.query_args = {'id': command_id}
        self.request()

    def request(self):
        print self.query_args
        encoded_args = urllib.urlencode(self.query_args)
        try:
            response = urllib2.urlopen(self.url, encoded_args)
        except urllib2.HTTPError, e:
            print e.code
        except urllib2.URLError, e:
            print e.reason
        else:
            print response.read()


if __name__ == '__main__':
    cd ="194","/ZML/Dailies/20161129", "whad", "References"
    CallBack().dai_callback(cd[0], cd[1], cd[2], cd[3])
    CallBack().render_callback('23')
