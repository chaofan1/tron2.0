#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Filename: client.py
# Author: liangcy
# Created: 2016/12/14
# Latest Modified:
# Platform: windows
# Copyright: Illumina ltd, PTD department, 2016

# 192.168.1.85|x:/ZML/Dailies/20161129|zml01001_prd_liangcy_HVD_v0150|194|Dailies2

import socket
import os


def clientLink(data):
    args = data.split("|")
    clientIP = args[0]
    senStr = '|'.join(args[1:])
    filePath = ""
    if len(args) > 2:
        filePath = args[1]

    HOST = clientIP
    PORT = 29400
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    if senStr:
        s.sendall(senStr)
        print('already send info')
        if data.endswith('Dailies1') or data.endswith('Dailies2'):
            serverName = "/Tron"
            data = s.recv(1024)
            data_replace = data.replace('\\', '/')
            filePath_replace = filePath.replace('\\', '/')
            if os.path.exists(serverName+data_replace):
                os.chmod((serverName+data_replace), 0755)
                os.chmod((serverName + filePath_replace), 0755)
                print (serverName + data_replace)
            else:
                os.chmod((serverName + filePath_replace), 0755)
                print (serverName + filePath_replace)
        s.close()
        print('client close')
    return


if __name__ == '__main__':
    clientLink('')
