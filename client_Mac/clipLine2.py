# coding:utf8
import os
import subprocess
import shutil
from clipLine import to_php
import sys
import config
reload(sys)
sys.setdefaultencoding('utf-8')


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
    ffmpeg = config.ffmpeg
    command = "%s -i %s -i %s -loglevel -8 -y -g 2 -keyint_min 2 -filter_complex " % (ffmpeg, backup_mov, input_img) + \
              repr("[0:v][1:v]overlay=enable='between(n,%s,%s)'") % (frame, frame) + " -acodec copy %s" % output_mov
    su = subprocess.Popen(command, shell=True)
    su.wait()
    if 'exists' in backup_mov:
        os.remove(backup_mov)


class Pack(object):
    def __init__(self):
        self.task = 'pack'
        self.ration1 = 'Stuff/cmp/publish'
        self.ration2 = 'geo'

    def pack(self, pro_scene, out_path):
        if os.path.exists(pro_scene):
            shot_li = os.listdir(pro_scene)
            if shot_li:
                shot_li = [i for i in shot_li if not i.startswith('.') and i.isdigit()]
                queue_len = len(shot_li)  # 任务总量
                if shot_li:
                    for ind, shot in enumerate(shot_li):
                        pub = os.path.join(pro_scene, shot, self.ration1)    # /Post/FUY/001/001/Stuff/cmp/publish
                        if os.path.exists(pub):
                            producer_paths = os.listdir(pub)
                            if producer_paths:
                                producer_paths = [i for i in producer_paths if not i.startswith('.')]
                                for producer_path in producer_paths:
                                    path = os.path.join(pub, producer_path, self.ration2)  # /Post/FUY/001/001/Stuff/cmp/publish/geo
                                    if os.path.exists(path):
                                        files = os.listdir(path)
                                        if files:
                                            files = [i for i in files if not i.startswith('.')]
                                            for file_ in files:
                                                mov_path = os.path.join(path, file_)  # /Post/FUY/001/001/Stuff/cmp/publish/geo/...mov
                                                if file_.endswith('mov'):
                                                    shutil.copy(mov_path, out_path)
                                                    print mov_path + '  >>  ' + out_path
                                                elif os.path.isdir(mov_path):
                                                    out_copy_path = out_path+'/'+file_
                                                    shutil.copytree(mov_path, out_copy_path)
                                                    print mov_path + '  >>  ' + out_copy_path
                                        else:
                                            print(path, "为空")
                                    else:
                                        print path,' not exists'
                            else:
                                print(pub, "为空")
                            qsize = queue_len - ind - 1  # 当前剩余任务数
                            to_php(queue_len, qsize, '', '', '', self.task)
                        else:
                            print pub,' not exists'
                else:
                    print pro_scene,'中没有镜头'
        else:
            print pro_scene,' not exists'
