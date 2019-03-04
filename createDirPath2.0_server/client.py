#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# 192.168.1.85|x:/ZML/Dailies/20161129|zml01001_prd_liangcy_HVD_v0150|194|Dailies2

import socket
import os
import config
import fcntl
import time
import shutil
from createFolder import TronFolder
from server_callback import CallBack


def clientLink(data):
    args = data.split("|")
    task = args[-1]
    senStr = '|'.join(args[1:])
    server_all = config.All
    log_path_client = config.log_path_client + time.strftime("%Y%m%d") + '.log'
    HOST = args[0]
    PORT = config.port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
    except:
        write_log(log_path_client, HOST+':'+PORT+' can not connect'+'\n')
    else:
        if senStr:
            write_log(log_path_client, data+'\n')
            s.sendall(senStr)
            write_log(log_path_client, ' already send' + '\n')
            task_set = {'clip1','add_xml','clip2','download','Dailies1','Dailies2','lgt_dai','Reference'}
            if task in task_set:
                recv_data = s.recv(1024)
                s.close()
                write_log(log_path_client, 'client close' + '\n')
                if recv_data:
                    write_log(log_path_client, 'recv data is: ' + recv_data + '\n')
                    if task == 'clip2':
                        video_dir = os.path.dirname(args[1])
                        path = server_all + '/' + video_dir
                        os.chmod(path, 0555)
                        write_log(log_path_client, path + ' already chmod 555' + '\n')
                    elif task == 'Dailies1' or task == 'lgt_dai' or task == 'Dailies2':
                        filePath = args[1]
                        filename = args[2]
                        daiPath = server_all + filePath + '/img'  # /Tron/FUY/001/001/stuff/cmp/img
                        daiPath2 = server_all + filePath + '/mov'
                        dai_file_path = daiPath + '/' + filename
                        dai_file_path2 = daiPath2 + '/' + filename
                        if not os.listdir(dai_file_path):
                            os.chmod(daiPath, 0777)
                            os.rmdir(dai_file_path)
                        if not os.listdir(dai_file_path2):
                            os.chmod(daiPath2, 0777)
                            os.rmdir(dai_file_path2)
                        if os.path.exists(dai_file_path):
                            os.chmod(dai_file_path, 0755)
                        if os.path.exists(dai_file_path2):
                            os.chmod(dai_file_path2, 0755)
                        os.chmod(daiPath, 0555)
                        os.chmod(daiPath2, 0555)
                        write_log(log_path_client, daiPath + ' already chmod 555' + '\n')
                    elif task == 'Reference':
                        server_ref = config.Reference
                        ref_path = server_ref + args[1]
                        os.chmod(ref_path, 0555)
                        write_log(log_path_client, ref_path + ' already chmod 555' + '\n')
                    elif task == 'download':
                        return recv_data
                    elif task == 'clip1' or task == 'add_xml':
                        # args:[ip, xml_path, TXT/998/, project_id, seq_id, xml_id, command_id, clip1]
                        xml_path = args[1]                   # recv_data: FUY/001/
                        seq_path = server_all+'/'+recv_data  # /Tron/FUY/001/
                        if os.path.exists(seq_path):
                            shots_li = (i for i in os.listdir(seq_path) if i.isdigit())  # 获取场下的所有镜头号
                            proPath = seq_path[:-5]    # /Tron/FUY  项目路径
                            seqName = seq_path[-4:-1]    # 场号
                            it_uid = 11001
                            it_gid = 11000
                            for shotName in shots_li:
                                shot_path = seq_path+shotName
                                # 在镜头下创建Stuff和Work
                                TronFolder().CreateStuff(proPath, seqName, shotName, 'prd', '', '')
                                write_log(log_path_client, 'create stuff '+proPath+' / '+seqName+shotName+'\n')
                                work_path = shot_path + '/Work'
                                TronFolder().CreateFolder(work_path, "0555", "")
                                # 创建/Stuff/prd/plates/mov/tron_plates文件夹，用于存放tron的剪辑线素材
                                tron_plates_path = shot_path + '/Stuff/prd/plates/mov/tron_plates'
                                TronFolder().CreateFolder(tron_plates_path, "0555", "")
                                # 获取视频和图片路径，将视频和缩略图剪切至 /Stuff/prd/plates/mov/tron_plates
                                mov_jpg = [i for i in os.listdir(shot_path) if i.endswith('jpg') or i.endswith('mov')]
                                for mov_or_jpg in mov_jpg:
                                    mov_or_jpg_path = shot_path + '/' + mov_or_jpg
                                    shutil.move(mov_or_jpg_path, tron_plates_path)
                                # 修改每个镜头的权限为it 555
                                os.chown(shot_path, it_uid, it_gid)
                                os.chmod(shot_path, 0555)
                            os.chmod(seq_path, 0555)
                            xml_path = server_all+'/'+xml_path
                            os.remove(xml_path)
                            write_log(log_path_client, seq_path + ' already chmod 555' + '\n')
                            CallBack().clip_to_php(1, 0, args[3], args[4], args[5])
                            write_log(log_path_client, 'already callback 100' + '\n')


def write_log(log_path_client,info):
    with open(log_path_client, 'a') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        f.write(info)


if __name__ == '__main__':
    clientLink('192.168.102.168|DSN_TTT_27|download')
