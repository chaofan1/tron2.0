#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
# 将服务器执行成功的命令告诉数据库


import urllib
import urllib2


def callback(command_id):
    url_update = 'http://192.168.100.49/tron/index.php/python/renewScriptStatus'
    query_args = {'id': command_id}
    encoded_args = urllib.urlencode(query_args)
    try:
        urllib2.urlopen(url_update, encoded_args)
    except urllib2.HTTPError, e:
        print e.code
    except urllib2.URLError, e:
        print e.reason


# def disCallback(task_ids):
#     url_update = 'http://192.168.1.81/tron/index.php/python/add_download_link'
#     query_args = {'name': task_ids[0], 'task_ids': task_ids[1]}
#     encoded_args = urllib.urlencode(query_args)
#     try:
#         urllib2.urlopen(url_update, encoded_args)
#     except urllib2.HTTPError, e:
#         print e.code
#     except urllib2.URLError, e:
#         print e.reason


if __name__ == '__main__':
    callback(1)
