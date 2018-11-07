#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Filename: httpUrl.py
# 将数据返回给服务器

import urllib
import urllib2


class CallBack:
    def __init__(self):
        self.url = ''
        self.query_args = {}

    def dai_callback(self, ID, path, fileName, imgSize):
        self.url = 'http://192.168.1.117/callback/dailies'
        if imgSize:
            self.query_args = {'id': ID, 'path': path, 'filename': fileName, 'imgSize': imgSize}
        else:
            self.query_args = {'id': ID, 'path': path, 'filename': fileName}
        self.request()

    def render_callback(self, command_id):
        self.url = 'http://192.168.100.87/tron/index.php/python/renewScriptStatus'
        self.query_args = {'id': command_id}
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


if __name__ == '__main__':
    cd ="194","/ZML/Dailies/20161129", "whad", "References"
    CallBack().dai_callback(cd[0], cd[1], cd[2], cd[3])
    CallBack().render_callback('23')
