#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# 192.168.1.85|x:/ZML/Dailies/20161129|zml01001_prd_liangcy_HVD_v0150|194|Dailies2

import socket
import os,time
import logging
import config

logging.basicConfig(filename=config.log_path_server + time.strftime("%Y%m%d") + '.log', level=logging.INFO,
					format="%(asctime)s - %(levelname)s - %(message)s")


def clientLink(data):
    args = data.split("|")
    task = args[-1]
    senStr = '|'.join(args[1:])
    serverName = config.All

    HOST = args[0]
    PORT = 29401
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
    except:
        logging.info(HOST + ' can not connect')
    else:
        if senStr:
            s.sendall(senStr)
            logging.info('already send info' + '\n')
            task_set = {'clip1','add_xml','clip2','download','Dailies1','lgt_dai','Reference'}
            if task in task_set:
                data = s.recv(1024)
                if data:
                    logging.info('recv data is: ' + data)
                    if task == 'clip2':
                        video_dir = os.path.dirname(args[1])
                        path = serverName + '/' + video_dir
                        os.chmod(path, 0555)
                        logging.info(path + ' already chmod 555' + '\n')
                    elif task == 'Dailies1' or task == 'lgt_dai':
                        filePath = args[1]
                        filename = args[2]
                        daiPath = serverName + filePath + '/img'  # /Tron/FUY/001/001/stuff/cmp/img
                        daiPath2 = serverName + filePath + '/mov'
                        dai_file_path = daiPath + '/' + filename
                        dai_file_path2 = daiPath2 + '/' + filename
                        if not os.listdir(dai_file_path):
                            os.chmod(daiPath, 0777)
                            os.rmdir(dai_file_path)
                        if not os.listdir(dai_file_path2):
                            os.chmod(daiPath2, 0777)
                            os.rmdir(dai_file_path2)
                        if os.path.exists(dai_file_path):
                            os.chmod(dai_file_path, 0555)
                        if os.path.exists(dai_file_path2):
                            os.chmod(dai_file_path2, 0555)
                        os.chmod(daiPath, 0555)
                        os.chmod(daiPath2, 0555)
                    elif task == 'Reference':
                        server_ref = config.Reference
                        ref_path = server_ref + args[1]
                        os.chmod(ref_path, 0555)
                    elif task == 'download':
                        s.close()
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
    clientLink('192.168.102.168|DSN_TTT_27|download')
