#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# 192.168.1.85|x:/ZML/Dailies/20161129|zml01001_prd_liangcy_HVD_v0150|194|Dailies2

import socket
import os,time
import logging
from config import log_path

logging.basicConfig(filename=log_path + 'server_log/' + time.strftime("%Y%m%d") + '.log', level=logging.INFO,
					format="%(asctime)s - %(levelname)s - %(message)s")

def clientLink(data):
    args = data.split("|")
    clientIP = args[0]
    task = args[-1]
    senStr = '|'.join(args[1:])
    serverName = "/Tron"

    HOST = clientIP
    PORT = 29400
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    if senStr:
        s.sendall(senStr)
        logging.info('already send info' + '\n')
        if task == 'clip1' or task == 'add_xml' or task == 'clip2' or task == 'download':
            data = s.recv(1024)
            if task == 'clip2':
                video_dir = os.path.dirname(args[1])
                path = serverName + '/' + video_dir
                os.chmod(path, 0555)
                logging.info(path + ' already chmod 555' + '\n')
            elif task == 'download':
                return data
            else:
                xml_path = args[1]
                recv_path = data.replace('\\', '/')
                ser_recv_path = serverName+'/'+recv_path  # clip /Tron/FUY/001
                if os.path.exists(ser_recv_path):
                    ch_li = os.listdir(ser_recv_path)
                    for i in ch_li:
                        os.chmod(ser_recv_path+'/'+i, 0555)
                    os.chmod(ser_recv_path, 0555)
                    xml_path = serverName+'/'+xml_path
                    os.remove(xml_path)
                    logging.info(ser_recv_path + ' already chmod 555' + '\n')

        s.close()
        logging.info('client close' + '\n')



if __name__ == '__main__':
    clientLink('ip|tron_TXT_7|download')
