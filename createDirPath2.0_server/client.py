#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# 192.168.1.85|x:/ZML/Dailies/20161129|zml01001_prd_liangcy_HVD_v0150|194|Dailies2

import socket
import os


def clientLink(data):
    args = data.split("|")
    clientIP = args[0]
    xml_path = args[1]
    task = args[-1]
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
        # task_set1 = {'Dailies1', 'Dailies2', 'clip1', 'add_xml'}
        task_set1 = {'clip1', 'add_xml'}
        task_set2 = {'Dailies1', 'Dailies2'}
        task_set3 = {'clip1', 'add_xml'}
        if task in task_set1:
            serverName = "/Tron"
            data = s.recv(1024)
            recv_path = data.replace('\\', '/')
            ser_recv_path = serverName+recv_path  # Dailies /Tron/FUY/001/001/stuff/cmp/mov/filename
            if os.path.exists(ser_recv_path):
                # if task in task_set2:
                #     os.chmod(ser_recv_path, 0555)
                #     os.chmod((serverName+filePath+'/mov'), 0755)  # filePath /FUY/001/001/stuff/cmp/
                #     os.chmod((serverName+filePath+'/img'), 0755)  # filePath /FUY/001/001/stuff/cmp/
                if task in task_set3:
                    ch_li = os.listdir(ser_recv_path)
                    for i in ch_li:
                        os.chmod(ser_recv_path+'/'+i, 0555)
                    os.chmod(ser_recv_path, 0555)
                    xml_path = serverName + xml_path
                    os.remove(xml_path)
                print serverName+filePath+'/mov'
        s.close()
        print('client close')
    return


if __name__ == '__main__':
    clientLink('')
