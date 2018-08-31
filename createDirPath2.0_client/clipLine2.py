# coding:utf8
import xml.etree.cElementTree as et
from urllib import quote
import os
import subprocess
import pymysql
from shutil import copy
from clipLine import to_php
import re

ip = '127.0.0.1'
user_name = 'root'
passwd = 'Root123'
db_name = 'new_tron'
table_name = 'oa_approvals'


class BackInsert(object):
    def __init__(self):
        pass

    def insert(self,input_mov, input_img,frame,sql_id):
        # 为回插的视频重命名
        mov_name = os.path.basename(input_mov).split('.')
        mov_name_new = mov_name[0] + '_postil.' + mov_name[1]
        mov_path = os.path.dirname(input_mov)
        output_mov = os.path.join(mov_path,mov_name_new)
        frame = str(int(round(float(frame))))  # str(int(float(tim) * float(rate))-1)  # 计算要替换第几帧
        ffmpeg = 'ffmpeg'
        command = "%s -i %s -i %s -y -g 2 -keyint_min 2 -filter_complex " % (ffmpeg,input_mov, input_img) + \
                  repr("[0:v][1:v]overlay=enable='between(n,%s,%s)'") % (frame,frame) + " -acodec copy %s" % output_mov
        if '_postil.' in input_mov:
            su = subprocess.Popen(command, shell=True)
            su.wait()
            os.remove(input_mov)
            os.rename(output_mov, input_mov)
        else:
            subprocess.Popen(command, shell=True)
            self.update_sql(sql_id,output_mov)

    def update_sql(self,sql_id,output_mov):
        try:
            output_mov = re.search(r'.*(uploads.*)', output_mov).group(1)
            conn = pymysql.connect(ip,user_name, passwd, db_name, charset='utf8', use_unicode=True)
        except:
            print('connect fail')
        else:
            cursor = conn.cursor()
            insert_sql = "UPDATE %s SET file='%s' where id = %s" % (table_name,output_mov,sql_id)
            try:
                cursor.execute(insert_sql)
                conn.commit()
            except Exception as e:
                print(e)
            else:
                cursor.close()
                conn.close()


class Pack(object):
    def __init__(self):
        pass

    def pack(self,pro_scene,xml_path,out_path):
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        shot_li = os.listdir(pro_scene)
        if shot_li:
            shot_li = [i for i in shot_li if not i.startswith('.')]
            queue_len = len(shot_li)  # 任务总量
            task = 'pack'
            ration1 = 'Stuff/cmp/publish'
            for ind,shot in enumerate(shot_li):
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
                                    copy(mov_path,out_path)
                                    qsize = queue_len-ind-1  # 当前剩余任务数
                                    to_php(queue_len,qsize,'','','',task)  # 将任务进行的百分比传给PHP
                        else:
                            print(path, "为空")
                else:
                    print(pub,"为空")

            self.edit_xml(xml_path,out_path)

    def edit_xml(self,xml_path,out_path):
        tree = et.ElementTree(file=xml_path)
        paths_ele = tree.findall('.//pathurl')
        paths_ele = filter(lambda x: x.text.endswith('mov'), paths_ele)
        for pathurl in paths_ele:
            filename = pathurl.text.split('/')[-1]
            new_path = quote(os.path.join('file://localhost',out_path,filename))
            print(new_path)
            pathurl.text = new_path
        xml_name = xml_path.split('/')[-1]
        xml_path_new = os.path.join(out_path,xml_name)
        tree.write(xml_path_new)
