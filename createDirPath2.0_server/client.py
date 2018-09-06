#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

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
        if args[-1] == 'Dailies1' or args[-1] == 'Dailies2' or args[-1] == 'Reference' or args[-1] == 'clip1':
            serverName = "/Tron"
            data = s.recv(1024)
            recv_path = data.replace('\\', '/')
            if os.path.exists(serverName+recv_path):
                os.chmod((serverName + recv_path), 0755)
                if args[-1] != 'clip1':
                    os.chmod((serverName + filePath), 0755)
                print (serverName + recv_path)
        s.close()
        print('client close')
    return


if __name__ == '__main__':
    clientLink('')
