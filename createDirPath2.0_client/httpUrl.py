#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
# Filename: httpUrl.py
#将数据返回给服务器

import urllib
import urllib2


def toHttpask(ID, path, fileName, UpTask, imgSize):
    #print fileName
    if imgSize:
        query_args = {'id': ID, 'path': path, 'filename': fileName, 'imgSize': imgSize}
    else:
        query_args = {'id': ID, 'path': path, 'filename': fileName}
    encoded_args = urllib.urlencode(query_args)
    url = ""
    if UpTask == "Dailies1" or UpTask == "Dailies2":
        url = 'http://192.168.1.117/callback/dailies'
    elif UpTask == "References":
        url = 'http://192.168.1.117/callback/reference'
    print urllib2.urlopen(url, encoded_args).read()


def render_callback(command_id):
    url_update = 'http://192.168.100.87/tron/index.php/python/renewScriptStatus'
    query_args = {'id': command_id}
    encoded_args = urllib.urlencode(query_args)
    try:
        urllib2.urlopen(url_update, encoded_args)
    except urllib2.HTTPError, e:
        print e.code
    except urllib2.URLError, e:
        print e.reason


if __name__ == '__main__':
    cd ="194","/ZML/Dailies/20161129", "whad", "References"
    toHttpask(cd[0], cd[1], cd[2], cd[3])
