# coding:utf8
import xml.etree.cElementTree as et
from urllib import quote
import os
import subprocess
import pymysql
from shutil import copy
from clipLine import to_php
import re

ip = '192.168.100.49'
user_name = 'root'
passwd = 'king9188YJQ@'
db_name = 'new_tron'
table_name = 'oa_approvals'


def insert(output_mov, input_img, frame):
    # 为回插的视频重命名
    mov_name = os.path.basename(output_mov).split('.')
    mov_name_new = mov_name[0] + '_backup.' + mov_name[1]
    mov_path = os.path.dirname(output_mov)
    backup_mov = os.path.join(mov_path, mov_name_new)
    if os.path.exists(backup_mov):
        mov_name_new = mov_name[0] + '_exists.' + mov_name[1]
        backup_mov = os.path.join(mov_path, mov_name_new)
    os.rename(output_mov, backup_mov)
    frame = str(int(round(float(frame))))  # str(int(float(tim) * float(rate))-1)  # 计算要替换第几帧
    ffmpeg = 'ffmpeg'
    command = "%s -i %s -i %s -loglevel -8 -y -g 2 -keyint_min 2 -filter_complex " % (ffmpeg, backup_mov, input_img) + \
              repr("[0:v][1:v]overlay=enable='between(n,%s,%s)'") % (frame, frame) + " -acodec copy %s" % output_mov
    su = subprocess.Popen(command, shell=True)
    su.wait()
    if 'exists' in backup_mov:
        os.remove(backup_mov)


class Pack(object):
    def pack(self, pro_scene, xml_path, out_path):
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        shot_li = os.listdir(pro_scene)
        if shot_li:
            shot_li = [i for i in shot_li if not i.startswith('.')]
            queue_len = len(shot_li)  # 任务总量
            task = 'pack'
            ration1 = 'Stuff/cmp/publish'
            for ind, shot in enumerate(shot_li):
                pub = os.path.join(pro_scene, shot, ration1)
                producer_paths = os.listdir(pub)
                if producer_paths:
                    producer_paths = [i for i in producer_paths if not i.startswith('.')]
                    for producer_path in producer_paths:
                        ration2 = 'geo'
                        path = os.path.join(pub, producer_path, ration2)
                        files = os.listdir(path)
                        if files:
                            files = [i for i in files if not i.startswith('.')]
                            for file in files:
                                mov_path = os.path.join(path, file)
                                if file.endswith('mov'):
                                    copy(mov_path, out_path)
                                    qsize = queue_len-ind-1  # 当前剩余任务数
                                    to_php(queue_len, qsize, '', '', '', task)  # 将任务进行的百分比传给PHP
                        else:
                            print(path, "为空")
                else:
                    print(pub, "为空")

            self.edit_xml(xml_path, out_path)

    def edit_xml(self, xml_path, out_path):
        tree = et.ElementTree(file=xml_path)
        paths_ele = tree.findall('.//pathurl')
        paths_ele = filter(lambda x: x.text.endswith('mov'), paths_ele)
        for pathurl in paths_ele:
            filename = pathurl.text.split('/')[-1]
            new_path = quote(os.path.join('file://localhost', out_path, filename))
            print(new_path)
            pathurl.text = new_path
        xml_name = xml_path.split('/')[-1]
        xml_path_new = os.path.join(out_path, xml_name)
        tree.write(xml_path_new)
